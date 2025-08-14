import { describe, it, expect } from 'vitest';
import { mapFileListToUploadItemList } from './mapFileListToUploadItemList';

describe('mapFileListToUploadItemList', () => {
  it('maps File[] to UploadItem[] with idle status and 0 progress', () => {
    const files: File[] = [
      new File(['a'], 'a.pdf', { type: 'application/pdf' }),
      new File(['b'], 'b.docx', { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' }),
    ];
    const items = mapFileListToUploadItemList(files);
    expect(items).toHaveLength(2);
    expect(items[0].file.name).toBe('a.pdf');
    expect(items[0].status).toBe('idle');
    expect(items[0].progress).toBe(0);
    expect(typeof items[0].id).toBe('string');
  });
});


