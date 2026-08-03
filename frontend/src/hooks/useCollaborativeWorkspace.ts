import { useState, useEffect, useCallback, useRef } from "react";

export interface WorkspaceDoc {
  id: string;
  project_id: string;
  title: string;
  content: string;
  version: number;
  created_by_id?: string;
  last_edited_by_id?: string;
  created_at: string;
  updated_at: string;
  conflict?: boolean;
}

export interface CollaboratorCursor {
  userId: string;
  username: string;
  avatar?: string;
  cursorOffset: number;
  selectionStart?: number;
  selectionEnd?: number;
}

export interface ActiveCollaborator {
  userId: string;
  username: string;
  avatar?: string;
  online: boolean;
}

export function useCollaborativeWorkspace(
  projectId: string,
  currentUserId: string,
  username: string,
) {
  const [documents, setDocuments] = useState<WorkspaceDoc[]>([]);
  const [activeDocId, setActiveDocId] = useState<string | null>(null);
  const [activeDoc, setActiveDoc] = useState<WorkspaceDoc | null>(null);
  const [collaborators, setCollaborators] = useState<ActiveCollaborator[]>([]);
  const [cursors, setCursors] = useState<Record<string, CollaboratorCursor>>({});
  const [hasConflict, setHasConflict] = useState<boolean>(false);
  const [conflictMessage, setConflictMessage] = useState<string>("");
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [isConnected, setIsConnected] = useState<boolean>(false);

  const wsRef = useRef<WebSocket | null>(null);

  // Load initial documents
  const fetchDocuments = useCallback(async () => {
    try {
      const res = await fetch(`/api/v1/projects/${projectId}/workspace/docs`);
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents || []);
        if (data.documents && data.documents.length > 0 && !activeDocId) {
          setActiveDocId(data.documents[0].id);
          setActiveDoc(data.documents[0]);
        }
      }
    } catch {
      // Fallback mock document if backend unreachable
      const mockDoc: WorkspaceDoc = {
        id: "doc-1",
        project_id: projectId,
        title: "Project Notes & Architecture",
        content:
          "# Real-Time Collaborative Workspace\n\nWelcome team! Edit project notes together in real time.",
        version: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setDocuments([mockDoc]);
      setActiveDocId("doc-1");
      setActiveDoc(mockDoc);
    }
  }, [projectId, activeDocId]);

  useEffect(() => {
    fetchDocuments();
  }, [fetchDocuments]);

  // Connect WebSocket for real-time collab
  useEffect(() => {
    if (!projectId) return;

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/api/v1/collab?token=demo-token`;

    try {
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        ws.send(JSON.stringify({ type: "doc.join", project_id: projectId, doc_id: activeDocId }));
      };

      ws.onmessage = (evt) => {
        try {
          const msg = JSON.parse(evt.data);
          if (msg.type === "doc.updated") {
            if (msg.doc_id === activeDocId) {
              setActiveDoc((prev) =>
                prev
                  ? {
                      ...prev,
                      title: msg.title ?? prev.title,
                      content: msg.content ?? prev.content,
                      version: msg.version ?? prev.version + 1,
                    }
                  : prev,
              );
            }
            setDocuments((prev) =>
              prev.map((d) =>
                d.id === msg.doc_id
                  ? {
                      ...d,
                      title: msg.title ?? d.title,
                      content: msg.content ?? d.content,
                      version: msg.version ?? d.version + 1,
                    }
                  : d,
              ),
            );
          } else if (msg.type === "doc.conflict") {
            setHasConflict(true);
            setConflictMessage(msg.message || "Conflict detected during edit.");
          } else if (msg.type === "doc.cursor_moved") {
            if (msg.user_id !== currentUserId) {
              setCursors((prev) => ({
                ...prev,
                [msg.user_id]: {
                  userId: msg.user_id,
                  username: msg.username || "Collaborator",
                  cursorOffset: msg.cursor_offset || 0,
                  selectionStart: msg.selection_start,
                  selectionEnd: msg.selection_end,
                },
              }));
            }
          }
        } catch {
          // Ignore decode error
        }
      };

      ws.onclose = () => {
        setIsConnected(false);
      };

      return () => {
        ws.close();
      };
    } catch {
      setIsConnected(false);
    }
  }, [projectId, activeDocId, currentUserId]);

  const selectDocument = (docId: string) => {
    setActiveDocId(docId);
    const found = documents.find((d) => d.id === docId) || null;
    setActiveDoc(found);
    setHasConflict(false);
  };

  const createDocument = async (title: string = "Untitled Document") => {
    try {
      const res = await fetch(`/api/v1/projects/${projectId}/workspace/docs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, content: "" }),
      });
      if (res.ok) {
        const newDoc = await res.json();
        setDocuments((prev) => [newDoc, ...prev]);
        setActiveDocId(newDoc.id);
        setActiveDoc(newDoc);
        return newDoc;
      }
    } catch {
      const newDoc: WorkspaceDoc = {
        id: `doc-${Date.now()}`,
        project_id: projectId,
        title,
        content: "",
        version: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };
      setDocuments((prev) => [newDoc, ...prev]);
      setActiveDocId(newDoc.id);
      setActiveDoc(newDoc);
      return newDoc;
    }
  };

  const updateContent = (content: string, title?: string) => {
    if (!activeDoc) return;
    setIsSaving(true);

    const updatedDoc: WorkspaceDoc = {
      ...activeDoc,
      title: title !== undefined ? title : activeDoc.title,
      content,
      version: activeDoc.version + 1,
    };

    setActiveDoc(updatedDoc);
    setDocuments((prev) => prev.map((d) => (d.id === activeDoc.id ? updatedDoc : d)));

    // Send real-time WS edit broadcast
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(
        JSON.stringify({
          type: "doc.edit",
          project_id: projectId,
          doc_id: activeDoc.id,
          title: updatedDoc.title,
          content: updatedDoc.content,
          base_version: activeDoc.version,
        }),
      );
    }

    setTimeout(() => setIsSaving(false), 400);
  };

  const updateCursor = (cursorOffset: number, selectionStart?: number, selectionEnd?: number) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN && activeDocId) {
      wsRef.current.send(
        JSON.stringify({
          type: "doc.cursor",
          project_id: projectId,
          doc_id: activeDocId,
          cursor_offset: cursorOffset,
          selection_start: selectionStart,
          selection_end: selectionEnd,
        }),
      );
    }
  };

  return {
    documents,
    activeDoc,
    activeDocId,
    collaborators,
    cursors,
    hasConflict,
    conflictMessage,
    isSaving,
    isConnected,
    selectDocument,
    createDocument,
    updateContent,
    updateCursor,
    dismissConflict: () => setHasConflict(false),
  };
}
