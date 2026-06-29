import { Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import ProtectedRoute from "./components/ProtectedRoute";
import Upload from "./pages/Upload";
import Documents from "./pages/Documents";
function App() {
  return (
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
    path="/dashboard"
    element={
        <ProtectedRoute>
            <Dashboard/>
        </ProtectedRoute>
    }
/>
<Route
    path="/upload"
    element={
        <ProtectedRoute>
            <Upload/>
        </ProtectedRoute>
    }
/>
<Route
    path="/documents"
    element={
        <ProtectedRoute>
            <Documents />
        </ProtectedRoute>
    }
/>
    </Routes>
  );
}

export default App;