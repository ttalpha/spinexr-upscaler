import { useEffect, useState } from 'react'
import Store from 'electron-store'
import { v4 } from 'uuid'

Store.initRenderer()
const store = new Store<{ userId?: string }>()

export const useAnonUserId = () => {
  const [userId, setUserId] = useState<string | null>(null)

  useEffect(() => {
    // @ts-ignore
    let savedUserId = store.get('userId') as string | undefined
    if (!savedUserId) {
      savedUserId = v4()
      // @ts-ignore
      store.set('userId', savedUserId)
    }
    setUserId(savedUserId)
  }, [])

  return { userId }
}
