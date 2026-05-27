import { useCallback, useEffect, useRef, useState } from "react";

type State<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
};

// Hook generico de fetch con refetch on-demand. Cancela actualizaciones
// si el componente se desmonta entre la llamada y la respuesta.
export function useFetch<T>(fetcher: () => Promise<T>) {
  const [state, setState] = useState<State<T>>({
    data: null,
    loading: true,
    error: null,
  });

  const mountedRef = useRef(true);
  const fetcherRef = useRef(fetcher);
  fetcherRef.current = fetcher;

  const run = useCallback(async () => {
    setState((s) => ({ ...s, loading: true, error: null }));
    try {
      const data = await fetcherRef.current();
      if (mountedRef.current) {
        setState({ data, loading: false, error: null });
      }
    } catch (err) {
      if (mountedRef.current) {
        const msg = err instanceof Error ? err.message : "Error desconocido";
        setState((s) => ({ ...s, loading: false, error: msg }));
      }
    }
  }, []);

  useEffect(() => {
    mountedRef.current = true;
    run();
    return () => {
      mountedRef.current = false;
    };
  }, [run]);

  return { ...state, refetch: run };
}
