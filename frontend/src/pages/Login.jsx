import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import api from "../services/api";

function Login() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);

    const navigate = useNavigate();

    const handleLogin = async () => {

        if (!email || !password) {
            alert("Please fill all fields");
            return;
        }

        try {

            setLoading(true);

            const response = await api.post("/login", {
                email,
                password
            });

            localStorage.setItem(
                "token",
                response.data.access_token
            );

            navigate("/dashboard");

        } catch (error) {

            if (error.response) {
                alert(error.response.data.detail);
            } else {
                alert("Unable to connect to server");
            }

        } finally {

            setLoading(false);

        }

    };

    return (

        <div
            className="container-fluid vh-100 d-flex justify-content-center align-items-center bg-light"
        >

            <div
                className="card shadow-lg p-4"
                style={{ width: "430px", borderRadius: "15px" }}
            >

                <h2 className="text-center text-primary mb-3">
                    Secure Employee Knowledge Assistant
                </h2>

                <p className="text-center text-muted">
                    Login to continue
                </p>

                <div className="mb-3">

                    <label className="form-label">
                        Email
                    </label>

                    <input
                        type="email"
                        className="form-control"
                        placeholder="Enter Email"
                        value={email}
                        onChange={(e) =>
                            setEmail(e.target.value)
                        }
                    />

                </div>

                <div className="mb-3">

                    <label className="form-label">
                        Password
                    </label>

                    <div className="input-group">

                        <input
                            type={showPassword ? "text" : "password"}
                            className="form-control"
                            placeholder="Enter Password"
                            value={password}
                            onChange={(e) =>
                                setPassword(e.target.value)
                            }
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

                <button
                    className="btn btn-primary w-100"
                    onClick={handleLogin}
                    disabled={loading}
                >

                    {
                        loading
                            ? "Logging In..."
                            : "Login"
                    }

                </button>

                <p className="text-center mt-3">

                    Don't have an account?

                    <Link
                        to="/register"
                        className="text-decoration-none ms-2"
                    >

                        Register

                    </Link>

                </p>

            </div>

        </div>

    );

}

export default Login;