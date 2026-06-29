import { useEffect, useState } from "react";
import api from "../services/api";

function Documents() {

    const [documents, setDocuments] = useState([]);
const [search, setSearch] = useState("");
    const loadDocuments = async () => {

        try {

            const token = localStorage.getItem("token");

            const response = await api.get(
                "/documents",
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            setDocuments(response.data.documents);

        }

        catch (error) {

            console.log(error);

        }

    };

    const deleteDocument = async (filename) => {

        if (!window.confirm("Delete this document?")) {
            return;
        }

        try {

            const token = localStorage.getItem("token");

            await api.delete(
                `/documents/${filename}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            alert("✅ Document deleted successfully");

            loadDocuments();

        }

        catch (error) {

            console.log(error);

            alert("❌ Delete failed");

        }

    };

    useEffect(() => {

        loadDocuments();

    }, []);
    const filteredDocuments = documents.filter((document) =>
    document.toLowerCase().includes(search.toLowerCase())
);

    return (

        <div className="container mt-5">
<div className="mb-4">

    <input
        type="text"
        className="form-control"
        placeholder="🔍 Search documents..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
    />

</div>
            

            <h2>

                📄 My Documents

            </h2>

            <hr />

            {

                documents.length === 0 ?

                (

                    <div className="alert alert-warning">

                        No documents found.

                    </div>

                )

                :

                filteredDocuments.map((document, index) => (

                    <div
                        key={index}
                        className="card shadow-sm mb-3"
                    >

                        <div
                            className="card-body d-flex justify-content-between align-items-center"
                        >

                            <div>

                                <i className="bi bi-file-earmark-pdf-fill text-danger me-2"></i>

                                {document}

                            </div>

                            <button
                                className="btn btn-danger"
                                onClick={() => deleteDocument(document)}
                            >

                                <i className="bi bi-trash"></i>

                            </button>

                        </div>

                    </div>

                ))

            }

        </div>

    );

}

export default Documents;