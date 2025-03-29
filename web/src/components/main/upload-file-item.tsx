import { DocumentTextIcon, XMarkIcon } from "@heroicons/react/24/outline";
import { Card, CardContent } from "@/components/ui/card";
import { formatFileSize } from "@/utils/format-file-size";

interface FileItemProps {
  name: string;
  size: number;
  removeUploadedFile: (name: string) => void;
}

export const UploadFileItem = ({
  name,
  size,
  removeUploadedFile,
}: FileItemProps) => {
  return (
    <Card className="py-3 px-5 border-gray-200">
      <CardContent className="px-0 flex justify-between gap-x-8 items-center">
        <div className="flex gap-x-4 items-center">
          <DocumentTextIcon className="h-6 w-6 text-gray-700" />
          <div>
            <div className="line-clamp-1 font-medium text-sm">{name}</div>
            <div className="text-xs text-gray-600">{formatFileSize(size)}</div>
          </div>
        </div>
        <XMarkIcon
          onClick={() => removeUploadedFile(name)}
          className="h-5 w-5 text-gray-600 cursor-pointer"
        />
      </CardContent>
    </Card>
  );
};
