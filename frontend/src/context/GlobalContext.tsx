import React, { createContext, useContext, useReducer, ReactNode } from 'react';

interface GlobalState {
    userData: any; // Se define el tipo según las necesidades
    // Se agrega más propiedades según sea necesario
}

interface Action {
    type: string;
    payload?: any;
}

const initialState: GlobalState = {
    userData: null,
};

const GlobalContext = createContext<{
    state: GlobalState;
    dispatch: React.Dispatch<Action>;
} | undefined>(undefined);

const globalReducer = (state: GlobalState, action: Action): GlobalState => {
    switch (action.type) {
        case 'SET_USER_DATA':
            return { ...state, userData: action.payload };
        // Se agrega más casos según sea necesario
        default:
            return state;
    }
};

export const GlobalProvider = ({ children }: { children: ReactNode }) => {
    const [state, dispatch] = useReducer(globalReducer, initialState);

    return (
        <GlobalContext.Provider value={{ state, dispatch }}>
            {children}
        </GlobalContext.Provider>
    );
};

export const useGlobalContext = () => {
    const context = useContext(GlobalContext);
    if (!context) {
        throw new Error('useGlobalContext must be used within a GlobalProvider');
    }
    return context;
};