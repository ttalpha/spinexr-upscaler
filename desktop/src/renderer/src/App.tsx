import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './components/ui/card'
import { useAnonUserId } from './hooks/use-anon-user-id'
import { ClockIcon, SparklesIcon } from '@heroicons/react/24/outline'
import { Tabs } from '@radix-ui/react-tabs'
import { useCallback, useEffect, useState } from 'react'
import { FileRejection } from 'react-dropzone'
import { toast } from 'sonner'
import { Dropzone } from './components/main/dropzone'
import { UploadFileItem } from './components/main/upload-file-item'
import { Button } from './components/ui/button'
import { Toaster } from './components/ui/sonner'
import { TabsContent, TabsList, TabsTrigger } from './components/ui/tabs'
import { HistoryList } from './components/history/history-list'
import { cn } from './lib/utils'
import { HistoryFile } from './types/history-file'
import optimizing from './assets/optimizing.svg'

function App() {
  const [historyFiles, setHistoryFiles] = useState<HistoryFile[]>([])
  const [loading, setLoading] = useState(false)

  const { userId } = useAnonUserId()
  const [files, setFiles] = useState<File[]>([])
  const [tab, setTab] = useState('upscale')
  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles(acceptedFiles)
  }, [])

  const removeUploadedFile = useCallback((filename: string) => {
    setFiles((prev) => prev.filter((file) => file.name !== filename))
  }, [])

  const onDropRejected = useCallback((rejectedFiles: FileRejection[]) => {
    const allErrors = new Set<string>()
    rejectedFiles.forEach((f) => f.errors.forEach((e) => allErrors.add(e.message)))

    const errorList = Array.from(allErrors)
    toast.error('Files upload error', {
      description: (
        <ul className="text-gray-600">
          {errorList.map((error) => (
            <li>{error}</li>
          ))}
        </ul>
      )
    })
  }, [])

  useEffect(() => {
    const fetchHistoryFiles = async () => {
      if (!userId) return
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/${userId}/images`)
        const data = await res.json()
        setHistoryFiles(data?.images || [])
      } catch (error) {
        toast.error('Failed to fetch history files')
      }
    }
    fetchHistoryFiles()
  }, [userId])

  const onFilesSubmit = useCallback(async () => {
    if (!userId) {
      toast.error('Submit files error', {
        description: 'User ID missing. Please refresh the page to generate one'
      })
      return
    }

    const submitData = new FormData()
    setLoading(true)
    for (const file of files) {
      submitData.append('file', file)
    }
    submitData.append('userId', userId)
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
        method: 'POST',
        body: submitData
      })
      const data = await res.json()
      const files: HistoryFile[] = data.files
      toast.success('Your DICOM files have been enhanced successfully')
      setHistoryFiles((prev) => [...files.map((image) => ({ ...image, recent: true })), ...prev])
      setFiles([])
      setTab('history')
    } catch (error) {
      toast.error('Something went wrong')
    } finally {
      setLoading(false)
    }
  }, [files, userId])
  return (
    <main className="h-screen bg-white px-4 sm:px-6 lg:px-8 py-8">
      <Toaster />
      <div className="mx-auto max-w-xl container">
        <Tabs value={tab} onValueChange={setTab}>
          <Card className="bg-white shadow-none w-full border-0">
            <TabsList className="w-full mb-4">
              <TabsTrigger value="upscale" className="flex gap-x-3 items-center">
                <SparklesIcon className="h-5 w-5" />
                Enhancer
              </TabsTrigger>
              <TabsTrigger value="history" className="flex gap-x-3 items-center">
                <ClockIcon className="h-5 w-5" />
                History
                <div className="h-5 min-w-5 bg-red-500 text-white rounded-full">
                  {historyFiles.length}
                </div>
              </TabsTrigger>
            </TabsList>
            <div>
              <div className="relative flex flex-col justify-center overflow-hidden bg-white">
                <div className="absolute inset-0 bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
                <div
                  className={cn(
                    loading && tab === 'upscale' && 'border border-gray-200',
                    'relative z-10 flex w-full cursor-pointer items-center overflow-hidden rounded-xl p-[1.5px]'
                  )}
                >
                  {loading && tab === 'upscale' && (
                    <div className="animate-moving-border absolute inset-0 h-full w-full rounded-full bg-[conic-gradient(#0ea5e9_20deg,transparent_120deg)]" />
                  )}
                  <div className="relative z-20 w-full rounded-[0.60rem] bg-white p-4">
                    <CardHeader className="px-0">
                      <CardTitle>Spine X-ray Resolution Enhancer</CardTitle>
                      <CardDescription>
                        {tab === 'upscale'
                          ? loading
                            ? 'Your images are being processed. This could take a few minutes'
                            : 'Select DICOM files you want to enhance the resolution'
                          : 'Your files will be saved up to 24 hours. After which, they will be deleted.'}
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="px-0">
                      <TabsContent className="grid gap-y-4 mt-6" value="upscale">
                        {loading ? (
                          <>
                            <div className="flex flex-col items-center justify-center gap-y-4">
                              <img
                                src={optimizing}
                                height="250px"
                                width="250px"
                                className="mx-auto"
                              />
                              <span className="text-sm font-medium text-gray-900"></span>
                            </div>
                          </>
                        ) : (
                          <>
                            <Dropzone
                              options={{
                                onDrop,
                                onDropRejected,
                                accept: {
                                  'application/dicom': ['.dcm', '.dicom']
                                },
                                maxFiles: 3,
                                multiple: true
                              }}
                            />
                            <ul className="mt-6 grid gap-4">
                              {files.map((file) => (
                                <li>
                                  <UploadFileItem
                                    removeUploadedFile={removeUploadedFile}
                                    name={file.name}
                                    size={file.size}
                                  />
                                </li>
                              ))}
                            </ul>
                            {files.length > 0 && (
                              <div className="mt-4 flex justify-end gap-x-3">
                                <Button onClick={() => setFiles([])} variant="secondary">
                                  Reset
                                </Button>
                                <Button onClick={onFilesSubmit}>Submit</Button>
                              </div>
                            )}
                          </>
                        )}
                      </TabsContent>
                      <TabsContent value="history">
                        <HistoryList userId={userId} historyFiles={historyFiles} />
                      </TabsContent>
                    </CardContent>
                  </div>
                </div>
              </div>
            </div>
          </Card>
        </Tabs>
      </div>
    </main>
  )
}

export default App
