import { http, HttpResponse, delay } from 'msw';
import { filesApiPaths } from '@entities/files/apiPaths';

type Options = {
  mode?: 'success' | 'error' | 'loading';
  status?: number;
  delayMs?: number;
};

export const createFilesHandlers = (opts: Options = {}) => {
  const { mode = 'success', status = 500, delayMs = 300 } = opts;
  return [
    http.post(filesApiPaths.root, async () => {
      if (mode === 'loading') {
        await delay(delayMs);
      }
      if (mode === 'error') {
        return HttpResponse.json({ message: 'Upload failed' }, { status });
      }
      return HttpResponse.json({ result: [1, 2] });
    }),
  ];
};


