import { config } from "@shared/config/env";

export const openSse = (
  path: string,
  onMessage: (e: MessageEvent) => void,
  onError?: (e: Event) => void
) => {
  const es = new EventSource(`${config.baseUrl}/${path}`);
  es.onmessage = onMessage;
  es.onerror = (e) => {
    if (onError) onError(e);
  };
  return es;
};
