import {create} from 'zustand';
import createAuthSlice from './authSlice';

export const useAppstore = create((...a)=>({...createAuthSlice(...a)}));
