/* eslint-disable @typescript-eslint/ban-ts-comment */
// @ts-nocheck
import { createFileRoute } from '@tanstack/react-router';
import { EmailTemplatePreviewer } from '../../components/admin/EmailTemplatePreviewer';

export const Route = createFileRoute('/_app/admin/email-templates')({
  component: AdminEmailTemplatesPage,
});

function AdminEmailTemplatesPage() {
  return (
    <div className="container mx-auto py-8 px-4">
      <EmailTemplatePreviewer />
    </div>
  );
}
