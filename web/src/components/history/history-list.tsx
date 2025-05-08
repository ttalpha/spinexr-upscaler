import { HistoryFile } from "@/types/history-file";
import { DownloadFileItem } from "@/components/main/download-file-item";
import noDataImage from "@/assets/no_data.svg";

interface HistoryListProps {
  historyFiles: HistoryFile[];
  userId: string | null;
}

export const HistoryList = ({ historyFiles, userId }: HistoryListProps) => {
  const groupFilesByDate = (files: HistoryFile[]) => {
    const groupedFiles: { [key: string]: HistoryFile[] } = {};
    files.forEach((file) => {
      const date = new Date(+file.timestamp).toLocaleString("en-US");
      if (!groupedFiles[date]) {
        groupedFiles[date] = [];
      }
      groupedFiles[date].push(file);
    });
    return groupedFiles;
  };
  const groupedFiles = groupFilesByDate(historyFiles);
  const sortedDates = Object.keys(groupedFiles).sort(
    (a, b) => new Date(b).getTime() - new Date(a).getTime()
  );

  if (historyFiles.length === 0)
    return (
      <div className="mt-6 flex flex-col items-center justify-center gap-y-4">
        <img
          src={noDataImage}
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
      {sortedDates.map((date) => (
        <li key={date}>
          <h3 className="text-sm mb-3 font-medium text-gray-900">{date}</h3>
          <ul className="grid gap-4">
            {groupedFiles[date].map((file) => (
              <DownloadFileItem
                timestamp={file.timestamp}
                recent={file.recent}
                userId={userId}
                key={`${file.timestamp}_${file.filename}`}
                name={file.filename}
                size={file.size}
              />
            ))}
          </ul>
        </li>
      ))}
    </ul>
  );
};
