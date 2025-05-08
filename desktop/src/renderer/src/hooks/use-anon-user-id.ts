import { useEffect, useState } from 'react'
import Store from 'electron-store'
import { v4 } from 'uuid'

const store = new Store()

export const useAnonUserId = () => {
  const [userId, setUserId] = useState<string | null>(null)

  useEffect(() => {
    let savedUserId = store.get('userId') as string | undefined
    if (!savedUserId) {
      savedUserId = v4()
      store.set('userId', savedUserId)
    }
    setUserId(savedUserId)
  }, [])

  return { userId }
}
