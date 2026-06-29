import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import api from "../services/api";

function Register() {

    const navigate = useNavigate();

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("Employee");
    const [adminCode, setAdminCode] = useState("");
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const handleRegister = async () => {

        if (!name || !email || !password) {
            alert("Please fill all fields");
            return;
        }

        try {

            setLoading(true);

            await api.post("/register", {
                name,
                email,
                password,
                role,
                admin_code: adminCode
            });

            alert("Registration Successful");

            navigate("/");

        } catch (error) {

            if (error.response) {
                alert(error.response.data.detail);
            }
            else {
                alert("Server Error");
            }

        }
        finally {

            setLoading(false);

        }

    };

    return (

        <div className="container-fluid vh-100 d-flex justify-content-center align-items-center bg-light">

            <div
                className="card shadow-lg p-4"
                style={{ width: "450px", borderRadius: "15px" }}
            >

                <h2 className="text-center text-success">
                    Create Account
                </h2>

                <p className="text-center text-muted">
                    Register a new user
                </p>

                <div className="mb-3">

                    <label>Name</label>

                    <input
                        className="form-control"
                        placeholder="Enter Name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                    />

                </div>

                <div className="mb-3">

                    <label>Email</label>

                    <input
                        type="email"
                        className="form-control"
                        placeholder="Enter Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />

                </div>

                <div className="mb-3">

                    <label>Password</label>

                    <div className="input-group">

                        <input
                            type={showPassword ? "text" : "password"}
                            className="form-control"
                            placeholder="Enter Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                        />

                        <button
                            type="button"
                            className="btn btn-outline-secondary"
                            onClick={() =>
                                setShowPassword(!showPassword)
                            }
                        >
                            {
                                showPassword
                                    ? <FaEyeSlash />
                                    : <FaEye />
                            }
                        </button>

                    </div>

                </div>

                <div className="mb-3">

                    <label>Role</label>

                    <select
                        className="form-select"
                        value={role}
                        onChange={(e) => setRole(e.target.value)}
                    >

                        <option>Employee</option>
                        <option>Manager</option>
                        <option>HR</option>
                        <option>CEO</option>

                    </select>

                </div>

                {(role === "Manager" ||
                    role === "HR" ||
                    role === "CEO") && (

                    <div className="mb-3">

                        <label>Admin Code</label>

                        <input
                            className="form-control"
                            placeholder="Enter Admin Code"
                            value={adminCode}
                            onChange={(e) =>
                                setAdminCode(e.target.value)
                            }
                        />

                    </div>

                )}

                <button
                    className="btn btn-success w-100"
                    onClick={handleRegister}
                    disabled={loading}
                >

                    {
                        loading
                            ? "Registering..."
                            : "Register"
                    }

                </button>

                <p className="text-center mt-3">

                    Already have an account?

                    <Link
                        to="/"
                        className="text-decoration-none ms-2"
                    >

                        Login

                    </Link>

                </p>

            </div>

        </div>

    );

}

export default Register;