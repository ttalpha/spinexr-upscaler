import { Card, CardContent } from '../ui/card'
import { formatFileSize } from '../../utils/format-file-size'
import { ArrowDownTrayIcon, DocumentTextIcon } from '@heroicons/react/24/outline'
import { useCallback } from 'react'
import { toast } from 'sonner'
import { Badge } from '../ui/badge'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '../ui/tooltip'

interface FileItemProps {
  name: string
  size: number
  timestamp: string
  recent: boolean
  userId: string | null
}

export const DownloadFileItem = ({ name, size, timestamp, userId, recent }: FileItemProps) => {
  const downloadFile = useCallback(async () => {
    try {
      if (!userId) {
        toast.error('Error downloading file', {
          description: (
            <div className="text-gray-600">
              User ID missing. Please refresh the page to generate one
            </div>
          )
        })
        return
      }
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/image/${userId}/${timestamp}/${name}`
      )
      const blob = await res.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = name
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)
    } catch (error) {
      toast.error('Something went wrong')
    }
  }, [])

  return (
    <Card className="py-3 px-5 border-gray-200">
      <CardContent className="px-0 flex justify-between gap-x-8 items-center">
        <div className="flex gap-x-4 items-center">
          <DocumentTextIcon className="h-6 w-6 text-gray-700" />
          <div>
            <div className="flex gap-x-2 items-center">
              <div className="line-clamp-1 font-medium text-sm">{name}</div>
              {recent && <Badge className="bg-blue-100 text-blue-900">New</Badge>}
            </div>
            <div className="text-xs text-gray-600">{formatFileSize(size)}</div>
          </div>
        </div>
        <Tooltip>
          <TooltipProvider>
            <TooltipTrigger asChild>
              <ArrowDownTrayIcon
                onClick={() => downloadFile()}
                className="h-5 w-5 text-gray-600 cursor-pointer"
              />
            </TooltipTrigger>
            <TooltipContent>Download</TooltipContent>
          </TooltipProvider>
        </Tooltip>
      </CardContent>
    </Card>
  )
}
