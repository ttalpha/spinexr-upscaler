import { HistoryFile } from "@/types/history-file";
import { DownloadFileItem } from "@/components/main/download-file-item";

interface HistoryListProps {
  historyFiles: HistoryFile[];
  userId: string | null;
}

export const HistoryList = ({ historyFiles, userId }: HistoryListProps) => {
  if (historyFiles.length === 0)
    return (
      <div className="flex flex-col items-center justify-center gap-y-4">
        <img
          src="src/assets/no_data.svg"
          height="150px"
          width="150px"
          className="mx-auto"
        />
        <span className="text-sm font-medium text-gray-900">
          You currently have no files.
        </span>
      </div>
    );
  return (
    <ul className="mt-6 grid gap-4">
      {historyFiles.map((file) => (
        <DownloadFileItem
          recent={file.recent}
          userId={userId}
          key={file.name}
          name={file.name}
          size={file.size}
        />
      ))}
    </ul>
  );
};
