// case: test-cases/Part_Detail_View/attachments-tab.md (UI-Detail_View-405)
import { test, expect } from '../../../fixtures';

test.use({ user: 'engineer' });

test.describe('Attachments tab', () => {
  test('UI-Detail_View-405: Attachments of one part are not listed on another part', { tag: ['@regression'] },
    async ({ partDetail, data }) => {
      const partA = await data.part(data.name('Attach A'), { description: 'Attachment isolation, part A' });
      const partB = await data.part(data.name('Attach B'), { description: 'Attachment isolation, part B' });
      const fileName = `${data.name('datasheet')}.pdf`.replace(/ /g, '-');

      // Pre-steps: log in (fixture), open part A's Attachments tab.
      await partDetail.open(Number(partA.pk));
      await partDetail.openTab('Attachments');

      await test.step('1. Upload the file to part A with Add attachment.', async () => {
        await partDetail.addAttachment(fileName, '%PDF-1.4 QA');
        await expect(partDetail.attachmentFileField).toContainText(fileName);
        await partDetail.form().submit();
        await expect(partDetail.attachmentLink(fileName)).toBeVisible();
      });

      await test.step('2. Open part B and its Attachments tab.', async () => {
        await partDetail.open(Number(partB.pk));
        await partDetail.openTab('Attachments');
        await expect(partDetail.noAttachmentsMessage).toBeVisible();
        await expect(partDetail.attachmentLink(fileName)).toBeHidden();
      });
    });
});
