import { api } from '../client';

export type EmailTemplateType =
  | 'welcome'
  | 'password_reset'
  | 'email_verification'
  | 'team_invitation'
  | 'project_accepted'
  | 'project_rejected'
  | 'weekly_digest';

export interface EmailTemplateInfo {
  template_type: EmailTemplateType;
  name: string;
  description: string;
  sample_context: Record<string, any>;
}

export interface EmailRenderResponse {
  template_type: EmailTemplateType;
  subject: string;
  html_content: string;
  text_content: string;
}

export const listEmailTemplates = async (): Promise<EmailTemplateInfo[]> => {
  return await api.get<EmailTemplateInfo[]>('/email-templates');
};

export const renderEmailTemplate = async (
  templateType: EmailTemplateType,
  context: Record<string, any> = {}
): Promise<EmailRenderResponse> => {
  return await api.post<EmailRenderResponse>('/email-templates/render', {
    template_type: templateType,
    context,
  });
};
