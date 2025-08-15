import { http, HttpResponse, delay } from 'msw';
import { filesApiPaths } from '@entities/files/apiPaths';
import type { ApiStatusCode } from '@shared/http/ApiStatusCode';

const url = `*${filesApiPaths.root}`

const success = http.post(url, async () =>
  HttpResponse.json({ result: [1, 2] })
);

const loading = (delayMs: number) =>
  http.post(url, async () => {
    await delay(delayMs);
    return HttpResponse.json({ result: [] });
  });

const error = (status: ApiStatusCode) =>
  http.post(url, async () =>
    HttpResponse.json({ message: 'Upload failed' }, { status })
  );

export const handlers = {
  default: success,
  loading,
  error,
};


