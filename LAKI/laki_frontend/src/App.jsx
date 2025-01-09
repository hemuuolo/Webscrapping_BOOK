import React from 'react'; 
import { Button } from '@/components/ui/button';
import Auth from './pages/auth';
import Chat from './pages/chat';
import Profile from './pages/profile';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
const App=()=> {
  
  return (
    
    <BrowserRouter>
    <Routes>
     <Route path='/auth' element={<Auth/>}></Route>
     <Route path='/chat' element={<Chat/>}></Route>
     <Route path='/profile' element={<Profile/>}></Route> 
     <Route path='*' element={<Auth/>}></Route>
    </Routes>
    </BrowserRouter>
    
  );
};

export default App;
