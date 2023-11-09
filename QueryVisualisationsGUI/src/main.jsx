import React from 'react'
import ReactDOM from 'react-dom/client'
import { ChakraProvider, extendTheme } from "@chakra-ui/react"

import { magicMerlionTheme } from '../theme.jsx'
import App from './App.jsx'
import './index.css'

const appTheme = extendTheme(magicMerlionTheme);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <ChakraProvider theme={appTheme}>
      <App />
    </ChakraProvider>
  </React.StrictMode>,
)
