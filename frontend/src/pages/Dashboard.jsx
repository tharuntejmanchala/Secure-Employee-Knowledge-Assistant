import { useEffect, useState } from "react";
import api from "../services/api";
import { useNavigate } from "react-router-dom";
function Dashboard() {

    const [user, setUser] = useState({});
    const [stats, setStats] = useState({});
    const [documents, setDocuments] = useState([]);

    const [question, setQuestion] = useState("");
    const [chatHistory, setChatHistory] = useState([]);
    const [asking, setAsking] = useState(false);
    const navigate = useNavigate();
    const loadDashboard = async () => {

        try {

            const token = localStorage.getItem("token");

            const config = {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            };

            const userResponse = await api.get(
                "/me",
                config
            );

            const statsResponse = await api.get(
                "/stats"
            );

            const documentsResponse = await api.get(
                "/documents",
                config
            );

            setUser(userResponse.data);
            setStats(statsResponse.data);
            setDocuments(documentsResponse.data.documents);

        }

        catch (error) {

            console.log(error);

        }

    };

    const askAI = async () => {

        if (!question.trim()) {

            alert("Please enter a question");

            return;

        }

        try {

            setAsking(true);

            const token = localStorage.getItem("token");

            const config = {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            };

            const response = await api.post(
                "/ask",
                {
                    question: question
                },
                config
            );

            setChatHistory((previous) => [

                ...previous,

                {
                    question: question,
                    answer: response.data.answer
                }

            ]);

            setQuestion("");

        }

        catch (error) {

            console.log(error);

            alert("Unable to get answer");

        }

        finally {

            setAsking(false);

        }

    };

    const logout = () => {

    localStorage.removeItem("token");

    window.location.href = "/";

};

    useEffect(() => {

        loadDashboard();

    }, []);

    return (

        <div className="container-fluid">

            <div className="row">

                {/* Sidebar */}

            <div
                className="col-2 bg-dark text-white vh-100 p-4 shadow-lg"
            >

                <div className="text-center mb-4">

    <i
        className="bi bi-robot fs-1 text-primary"
    ></i>

    <h3 className="mt-2">

        SEKA

    </h3>

</div>

                <hr/>

                <div
                    className="list-group"
                >

<button
    className="list-group-item list-group-item-action"
    onClick={() => navigate("/dashboard")}
>
    <i className="bi bi-speedometer2 me-2"></i>
    Dashboard
</button>

                    <button
                        className="list-group-item list-group-item-action"
                        onClick={() => navigate("/upload")}
                    >
                        <i className="bi bi-cloud-upload me-2"></i>
Upload
                    </button>

<button
    className="list-group-item list-group-item-action"
    onClick={() => navigate("/documents")}
>
    <i className="bi bi-folder2-open me-2"></i>
    Documents
</button>

<button
    className="list-group-item list-group-item-action"
    onClick={() =>
        document
            .getElementById("chat-section")
            ?.scrollIntoView({
                behavior: "smooth"
            })
    }
>
    <i className="bi bi-chat-dots me-2"></i>
    AI Chat
</button>

                    <button
                        className="list-group-item list-group-item-action text-danger"
                        onClick={logout}
                    >
                       <i className="bi bi-box-arrow-right me-2"></i>
Logout
                    </button>

                </div>

<div className="mt-auto pt-5 text-center">

    <hr/>

    <i
        className="bi bi-person-check-fill text-success"
        style={{ fontSize: "40px" }}
    ></i>

    <h6 className="mt-3">

        {user.name}

    </h6>

    <small className="text-secondary">

        Member Since

    </small>

    <br/>

    <span className="badge bg-primary mt-2">

        {user.joined_on}

    </span>

</div>

            </div>

{/* Main Content */}



<div
    className="col-10 p-4"
    style={{
        backgroundColor: "#f5f7fb",
        minHeight: "100vh"
    }}
>

    <div
        className="d-flex justify-content-between align-items-center mb-4"
    >

        <div>

            <h2
                className="fw-bold"
            >

                Welcome,

                <span className="text-primary">

                    {user.name}

                </span>

                👋

            </h2>

            <p
                className="text-muted mb-0"
            >

                {user.role} Dashboard

            </p>

        </div>

        <div>

            <span
                className="badge bg-success fs-6 px-3 py-2"
            >

                <i className="bi bi-circle-fill me-2"></i>

                Online

            </span>

        </div>

    </div>

    <hr />

                    {/* Cards */}

                    <div className="row">

<div className="col-md-4 mb-3">

    <div className="card border-0 shadow-lg rounded-4">

        <div className="card-body">

            <div className="d-flex justify-content-between">

                <div>

                    <p className="text-muted mb-1">

                        Total Users

                    </p>

                    <h2 className="fw-bold">

                        {stats.users}

                    </h2>

                </div>

                <div
                    className="bg-primary text-white rounded-circle d-flex align-items-center justify-content-center"
                    style={{
                        width: "60px",
                        height: "60px"
                    }}
                >

                    <i className="bi bi-people-fill fs-3"></i>

                </div>

            </div>

        </div>

    </div>

</div>
   <div className="col-md-4 mb-3">

    <div className="card border-0 shadow-lg rounded-4">

        <div className="card-body">

            <div className="d-flex justify-content-between">

                <div>

                    <p className="text-muted mb-1">

                        Documents

                    </p>

                    <h2 className="fw-bold">

                        {stats.documents}

                    </h2>

                </div>

                <div
                    className="bg-success text-white rounded-circle d-flex align-items-center justify-content-center"
                    style={{ width: "60px", height: "60px" }}
                >

                    <i className="bi bi-folder-fill fs-3"></i>

                </div>

            </div>

        </div>

    </div>

</div>
   <div className="col-md-4 mb-3">

    <div className="card border-0 shadow-lg rounded-4">

        <div className="card-body">

            <div className="d-flex justify-content-between align-items-center">

                <div>

                    <p className="text-muted mb-1">

                        Your Role

                    </p>

                    <h3 className="fw-bold">

                        {user.role}

                    </h3>

                </div>

                <div
                    className="bg-warning text-dark rounded-circle d-flex align-items-center justify-content-center"
                    style={{
                        width: "60px",
                        height: "60px"
                    }}
                >

                    <i className="bi bi-person-badge-fill fs-3"></i>

                </div>

            </div>

        </div>

    </div>

</div>

</div>
                    {/* Documents */}

                    <hr className="mt-5" />

 
<div className="d-flex justify-content-between align-items-center mt-5">

    <h4 className="fw-bold">

        <i className="bi bi-folder2-open text-warning me-2"></i>

        Accessible Documents

    </h4>
    

    <span className="badge bg-primary">

        {documents.length} Files

    </span>

</div>

<hr />
<div className="mt-3">

    {

        documents.length === 0 ?

        (

            <div className="alert alert-warning">

                No documents available.

            </div>

        )

        :

        documents.map((document, index) => (

            <div
                key={index}
                className="card shadow-sm border-0 rounded-4 mb-3"
            >

                <div
                    className="card-body d-flex justify-content-between align-items-center"
                >

                    <div>

                        <i className="bi bi-file-earmark-pdf-fill text-danger fs-4 me-3"></i>

                        <strong>

                            {document}

                        </strong>

                    </div>

                    <span
                        className="badge bg-success px-3 py-2"
                    >

                        Accessible

                    </span>

                </div>

            </div>

        ))

    }

</div>
                    {/* Chat */}

                    <hr className="mt-5" id="chat-section" />

<div className="d-flex justify-content-between align-items-center mt-5">

    <h4 className="fw-bold">

        <i className="bi bi-robot text-primary me-2"></i>

        AI Knowledge Assistant

    </h4>

    <span className="badge bg-info">

        Powered by Llama 3.2

    </span>

</div>

<hr/>
<textarea
    className="form-control rounded-4 shadow-sm"
    rows="4"
    placeholder="Ask a question about your documents..."
    value={question}
    onChange={(e) => setQuestion(e.target.value)}
></textarea>

                <button
    className="btn btn-primary rounded-pill px-5 py-2 mt-3 shadow"
    onClick={askAI}
    disabled={asking}
>

    {

        asking ?

        <>

            <span
                className="spinner-border spinner-border-sm me-2"
            ></span>

            Thinking...

        </>

        :

        <>

            <i className="bi bi-send-fill me-2"></i>

            Ask AI

        </>

    }

</button>

                    {/* AI Answer */}

<div className="mt-5">

    <h4 className="fw-bold">

        <i className="bi bi-chat-dots-fill me-2"></i>

        Conversation

    </h4>

    <div
        className="border rounded-4 p-4 mt-3"
        style={{
            maxHeight: "450px",
            overflowY: "auto",
            background: "#f8f9fa"
        }}
    >

        {

            chatHistory.length === 0 ?

            (

                <div className="text-center text-muted">

                    Start chatting with your AI assistant.

                </div>

            )

            :

            chatHistory.map((chat, index) => (

                <div
                    key={index}
                    className="mb-4"
                >

                    <div
                        className="d-flex justify-content-end"
                    >

                        <div
                            className="bg-primary text-white rounded-4 p-3"
style={{
    maxWidth:"75%",
    wordBreak:"break-word"
}}
                        >

                            <strong>

                                You

                            </strong>

                            <hr/>

                            {chat.question}

                        </div>

                    </div>

                    <div
                        className="d-flex justify-content-start mt-3"
                    >

                        <div
                            className="bg-white shadow rounded-4 p-3"
                            style={{
                                maxWidth: "75%"
                            }}
                        >

                            <strong>

                                🤖 AI Assistant

                            </strong>

                            <hr/>

                            {chat.answer}

                        </div>

                    </div>

                </div>

            ))

        }

    </div>

</div>

            </div> 

        </div>
<hr className="mt-5"/>

<div className="text-center text-muted">

    © 2026 Secure Employee Knowledge Assistant

    <br/>

    <small>

        Powered by FastAPI • React • Qdrant • Ollama

    </small>

</div>
    </div> 

);

}
export default Dashboard;