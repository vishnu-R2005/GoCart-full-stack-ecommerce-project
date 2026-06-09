import { createSlice } from '@reduxjs/toolkit'

const themeSlice = createSlice({
  name: 'theme',
  initialState: { darkMode: false },
  reducers: {
    toggleDarkMode: (state) => {
      state.darkMode = !state.darkMode
      document.documentElement.classList.toggle('dark', state.darkMode)
    },
    setDarkMode: (state, action) => {
      state.darkMode = action.payload
      document.documentElement.classList.toggle('dark', state.darkMode)
    },
  },
})

export const { toggleDarkMode, setDarkMode } = themeSlice.actions
export default themeSlice.reducer
