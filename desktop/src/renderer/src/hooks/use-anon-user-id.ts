import { useEffect, useState } from 'react'
import Store from 'electron-store'
import uniqid from 'uniqid'

const store = new Store()

export const useAnonUserId = () => {
  const [userId, setUserId] = useState<string | null>(null)

  useEffect(() => {
    let savedUserId = store.get('userId') as string | undefined
    if (!savedUserId) {
      savedUserId = uniqid()
      store.set('userId', savedUserId)
    }
    setUserId(savedUserId)
  }, [])

  return { userId }
}
