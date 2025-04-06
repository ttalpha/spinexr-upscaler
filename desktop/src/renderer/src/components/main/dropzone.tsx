import { DropzoneOptions, useDropzone } from 'react-dropzone'
import { cn } from '../../lib/utils'
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline'

interface DropzoneProps {
  options?: DropzoneOptions
}

export const Dropzone = ({ options }: DropzoneProps) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone(options)

  return (
    <div
      className={cn(
        isDragActive && 'bg-blue-100 border-blue-500',
        'h-40 flex items-center justify-center flex-col gap-3 w-full border-dashed border-2 border-gray-300 rounded'
      )}
      {...getRootProps()}
    >
      <input {...getInputProps()} />
      <ArrowUpTrayIcon className="text-gray-600 h-5 w-5" />
      <span className="font-medium text-sm">
        Drag &amp; drop or <span className="text-blue-500">choose file</span> to upload
      </span>
      <span className="text-xs text-gray-600">Accepted at most 3 DICOM files</span>
    </div>
  )
}
