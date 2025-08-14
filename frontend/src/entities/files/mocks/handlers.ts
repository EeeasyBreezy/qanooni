import { http, HttpResponse, delay } from 'msw';
import { filesApiPaths } from '@entities/files/apiPaths';
import type { ApiStatusCode } from '@shared/http/ApiStatusCode';

const success = http.post(filesApiPaths.root, async () =>
  HttpResponse.json({ result: [1, 2] })
);

const loading = (delayMs: number) =>
  http.post(filesApiPaths.root, async () => {
    await delay(delayMs);
    return HttpResponse.json({ result: [] });
  });

const error = (status: ApiStatusCode) =>
  http.post(filesApiPaths.root, async () =>
    HttpResponse.json({ message: 'Upload failed' }, { status })
  );

export const handlers = {
  default: success,
  loading,
  error,
};


