import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Upload() {

    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const navigate = useNavigate();

    const uploadDocument = async () => {

        if (!file) {
            alert("Please select a PDF file.");
            return;
        }

        try {

            setLoading(true);

            const token = localStorage.getItem("token");

            const formData = new FormData();

            formData.append("file", file);

            const response = await api.post(
                "/upload-document",
                formData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            alert("✅ " + response.data.message);

            navigate("/dashboard");

        }

        catch (error) {

            console.log(error);

            alert("❌ Upload Failed");

        }

        finally {

            setLoading(false);

        }

    };

    return (

        <div
            className="container d-flex justify-content-center align-items-center"
            style={{ minHeight: "100vh" }}
        >

            <div
                className="card shadow-lg border-0 rounded-4 p-5"
                style={{ width: "600px" }}
            >

                <div className="text-center">

                    <i
                        className="bi bi-cloud-upload-fill text-primary"
                        style={{ fontSize: "60px" }}
                    ></i>

                    <h2 className="mt-3">

                        Upload Document

                    </h2>

                    <p className="text-muted">

                        Upload PDF files for AI-powered semantic search

                    </p>

                </div>

                <hr />

                <div className="mb-4">

                    <label className="form-label fw-bold">

                        Select PDF File

                    </label>

                    <input
                        type="file"
                        accept=".pdf"
                        className="form-control"
                        onChange={(e) =>
                            setFile(e.target.files[0])
                        }
                    />

                </div>

                {

                    file &&

                    <div
                        className="alert alert-info"
                    >

                        <i className="bi bi-file-earmark-pdf-fill text-danger me-2"></i>

                        <strong>

                            Selected:

                        </strong>

                        {" "}

                        {file.name}

                    </div>

                }

                <button
                    className="btn btn-success rounded-pill py-2"
                    onClick={uploadDocument}
                    disabled={loading}
                >

                    {

                        loading ?

                        <>

                            <span
                                className="spinner-border spinner-border-sm me-2"
                            ></span>

                            Uploading...

                        </>

                        :

                        <>

                            <i className="bi bi-cloud-upload-fill me-2"></i>

                            Upload PDF

                        </>

                    }

                </button>

                <button
                    className="btn btn-outline-secondary rounded-pill mt-3"
                    onClick={() => navigate("/dashboard")}
                >

                    <i className="bi bi-arrow-left me-2"></i>

                    Back to Dashboard

                </button>

            </div>

        </div>

    );

}

export default Upload;