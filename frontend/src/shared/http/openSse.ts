export const openSse = (url: string, onMessage: (e: MessageEvent) => void, onError?: (e: Event) => void) => {
  const es = new EventSource(url);
  es.onmessage = onMessage;
  es.onerror = (e) => {
    if (onError) onError(e);
  };
  return es;
};


