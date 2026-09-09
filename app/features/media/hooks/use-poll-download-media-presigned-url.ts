import { useQuery } from "@tanstack/react-query";
import { createDownloadMediaPresignedURL } from "../api";
import { PresignedDownloadRequest } from "../schemas";
import { ApiError } from "@/lib/api/client";

const MAX_ATTEMPTS = 10;
const POLL_INTERVAL_MS = 3000;

export function usePollDownloadMediaPresignedURL(
  data: PresignedDownloadRequest,
  enabled: boolean,
) {
  return useQuery({
    queryKey: ["download-url", data.filename],
    queryFn: async () => {
      try {
        return await createDownloadMediaPresignedURL(data);
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          return null; // not ready yet — not an error state
        }
        throw err;
      }
    },
    enabled,
    refetchInterval: (query) => {
      // stop polling once we have a URL
      if (query.state.data?.url) return false;

      // stop polling after max attempts
      if (query.state.dataUpdateCount >= MAX_ATTEMPTS) return false;

      return POLL_INTERVAL_MS;
    },
    retry: false,
  });
}
