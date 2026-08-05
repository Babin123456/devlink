// @ts-nocheck
import { createFileRoute } from "@tanstack/react-router";
import { useState, useEffect } from "react";
import api from "@/lib/api";

export const Route = createFileRoute("/maintenance")({
  component: MaintenancePage,
});

function MaintenancePage() {
  const [maintenance, setMaintenance] = useState<{ message: string; end_time: string } | null>(
    null,
  );
  const [timeLeft, setTimeLeft] = useState<string>("");

  useEffect(() => {
    // Try to get maintenance info from local storage or an unauthenticated endpoint
    const checkMaintenance = async () => {
      try {
        const res = await api.get("/api/maintenance/active");
        setMaintenance(res.data);
      } catch (e: any) {
        // If 404, there is no active maintenance. We could redirect to home.
        if (e.response?.status === 404) {
          window.location.href = "/";
        } else if (e.response?.status === 503) {
          // The middleware caught it and returned 503 with data
          setMaintenance(e.response.data.maintenance);
        }
      }
    };
    checkMaintenance();
  }, []);

  useEffect(() => {
    if (!maintenance?.end_time) return;

    const interval = setInterval(() => {
      const now = new Date().getTime();
      const end = new Date(maintenance.end_time).getTime();
      const distance = end - now;

      if (distance < 0) {
        clearInterval(interval);
        setTimeLeft("Maintenance should be finishing up soon...");
        return;
      }

      const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
      const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((distance % (1000 * 60)) / 1000);

      setTimeLeft(`${hours}h ${minutes}m ${seconds}s remaining`);
    }, 1000);

    return () => clearInterval(interval);
  }, [maintenance]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-4">
      <div className="bg-white shadow-lg rounded-lg p-8 max-w-md w-full text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">Under Maintenance</h1>
        <p className="text-gray-600 mb-6">
          {maintenance?.message ||
            "The system is currently undergoing scheduled maintenance. Please check back later."}
        </p>

        {timeLeft && (
          <div className="bg-blue-50 text-blue-800 p-4 rounded-md">
            <p className="font-semibold text-lg">{timeLeft}</p>
          </div>
        )}
      </div>
    </div>
  );
}
