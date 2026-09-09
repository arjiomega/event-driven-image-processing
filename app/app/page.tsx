"use client";
import { useState } from "react";
import { useCreateProductMediaPresignedURL } from "@/features/media/hooks/use-create-presigned-url";
import { usePollDownloadMediaPresignedURL } from "@/features/media/hooks/use-poll-download-media-presigned-url";
import { uploadProductMedia } from "@/features/media/services/upload-media";
import Image from "next/image";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadedStorageKey, setUploadedStorageKey] = useState<string | null>(
    null,
  );
  const createPresignedURL = useCreateProductMediaPresignedURL();

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const onSubmit = async () => {
    if (!file) return;
    try {
      setUploading(true);
      const { storage_key } = await uploadProductMedia(
        file,
        async ({ filename, content_type }) => {
          return createPresignedURL.mutateAsync({
            data: { filename, content_type },
          });
        },
      );
      console.log("SUCCESSFULLY UPLOADED: ", storage_key);
      setUploadedStorageKey(storage_key);
      setFile(null);
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex flex-col flex-1 items-center justify-center font-sans bg-primary-content">
      <main className="">
        <div className="flex flex-row gap-4 items-stretch border-2 border-dotted bg-base-300">
          <div className="flex flex-col justify-end gap-2">
            <input
              type="file"
              className="file-input file-input-ghost"
              onChange={handleFileChange}
            />
            <button
              onClick={onSubmit}
              disabled={!file || uploading}
              className="btn w-full"
            >
              {uploading ? "Uploading..." : "Upload"}
            </button>
          </div>
          <div className="w-[300px] h-[300px] rounded-box border border-base-300 bg-base-200 flex items-center justify-center relative overflow-hidden">
            {uploadedStorageKey ? (
              <ProcessedMediaItem filename={uploadedStorageKey} />
            ) : (
              <span className="text-base-content/40 text-sm">
                Processed image will appear here
              </span>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

const MAX_ATTEMPTS = 10;

function ProcessedMediaItem({ filename }: { filename: string }) {
  const [attempts, setAttempts] = useState(0);
  const [prevDataUpdatedAt, setPrevDataUpdatedAt] = useState(0);
  const { data, dataUpdatedAt, refetch } = usePollDownloadMediaPresignedURL(
    { filename },
    true,
  );

  if (dataUpdatedAt !== prevDataUpdatedAt) {
    setPrevDataUpdatedAt(dataUpdatedAt);
    if (dataUpdatedAt) {
      setAttempts((a) => a + 1);
    }
  }

  const url = data?.url ?? null;
  const timedOut = !url && attempts >= MAX_ATTEMPTS;

  if (url) {
    return (
      <div className="relative w-full h-full">
        <Image
          src={url}
          alt="Processed Image"
          fill
          unoptimized
          className="w-full h-full object-contain"
        />
      </div>
    );
  }

  if (timedOut) {
    return (
      <div className="flex items-center gap-2">
        <span>{filename} — still processing</span>
        <button
          onClick={() => {
            setAttempts(0);
            refetch();
          }}
          className="btn btn-sm"
        >
          Retry
        </button>
      </div>
    );
  }

  return <span>{filename} — processing…</span>;
}
