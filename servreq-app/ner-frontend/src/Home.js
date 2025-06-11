import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
import "./App.css";
import NERText from "./NERText";

function Home() {
  const [inputText, setInputText] = useState("");
  const [entities, setEntities] = useState([]);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/ner", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ text: inputText }),
      });
      const data = await response.json();
      setEntities(data.entities);
    } catch (error) {
      setEntities([]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = async (e) => {
    e.preventDefault();
    setInputText("");
    setEntities([]);
    setLoading(false);
    navigate("/home");
  };

  return (
    <>
    <div style={{ margin: "5px", padding: "5px", textAlign: "left", fontSize: "1.2rem", padding: "1rem", borderLeft: "10px solid #40c6ed", borderBottom: "1px solid #40c6ed", zIndex: -1 }}>
      <i className="fa fa-comment-o" style={{ color: "#40c6ed" }}></i>
      <span style={{ marginLeft: "5px", fontWeight: "bold" }}>กรอกข้อมูลคำร้องขอบริการ</span>
    </div>
    <div style={{ maxWidth: "60%", margin: "auto", padding: "2rem" }}>
      <form onSubmit={handleSubmit}>
        <span style={{ fontSize: "0.8rem", color: "#888" }}>
          <i class="fa fa-info-circle" style={{ color: "#40c6ed" }}></i>
          <span style={{ marginLeft: "5px" }}> กรุณากรอกคำร้องขอบริการที่ต้องการวิเคราะห์</span>
        </span>
        <br />
        <textarea
          rows="4"
          cols="50"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="ระบุข้อมูลคำร้องบริการ..."
          style={{ width: "100%", padding: "1rem", fontSize: "1rem" }}
          required
        />
        <br />
        <div style={{ alignItems: "center", color: "#555", display: "flex", justifyContent: "center" }}>
          <button type="submit" disabled={loading} style={{ marginTop: "1rem", alignItems: "center", padding: "0.5rem", fontSize: "1rem", backgroundColor: "#40c6ed", color: "#fff", border: "none", borderRadius: "4px" }}>
            {loading ? "กำลังวิเคราะห์และบันทึกข้อมูล..." : "บันทึกข้อมูลคำร้องบริการ"}
          </button>
          <button onClick={handleClear} style={{ marginLeft: "0.2rem", marginTop: "1rem", alignItems: "center", padding: "0.5rem", fontSize: "1rem", backgroundColor: "#b1cdcd", color: "#fff", border: "none", borderRadius: "4px" }}>
            เคลียร์
          </button>
        </div>
      </form>

      {entities.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <NERText data={entities} formInput={inputText} />
        </div>
      )}
    </div>
    </>
  );
}

export default Home;
