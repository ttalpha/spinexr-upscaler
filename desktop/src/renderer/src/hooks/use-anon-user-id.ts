import { useEffect, useState } from 'react'
import { v4 } from 'uuid'

export const useAnonUserId = () => {
  const [userId, setUserId] = useState<string | null>(null)

  useEffect(() => {
    let savedUserId = localStorage.getItem('userId')
    if (!savedUserId) savedUserId = v4()
    setUserId(savedUserId)
  }, [])

  useEffect(() => {
    if (userId) localStorage.setItem('userId', userId)
  }, [userId])

  return { userId }
}
