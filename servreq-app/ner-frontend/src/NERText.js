import React, { useState, useEffect } from "react";
// Firebase configuration
import { db } from './config/firebaseConfig';
import { collection, addDoc, getDocs, deleteDoc, doc, serverTimestamp } from 'firebase/firestore';

const NERText = ({ data, formInput }) => {
    const [inputText, setInputText] = useState(formInput);
    const [text, setText] = useState(
      {
        "SrCreated" : null | "0000-00-00 00:00:00",
        "SrCreatedBy" : "",
        "SrDescription" : "",
        "SrId" : "",
        "SrNote" : "",
        "SrPriority" : "",
        "SrStatus" : 10,
        "SrUpdated" : null | "0000-00-00 00:00:00",
        "SrUpdatedBy" : ""
      }
    );

    // ฟังก์ชันสำหรับรวม token ย่อย (##) ให้เป็นคำเดียว
    const mergeTokens = (tokens) => {
        const merged = [];
        let currentToken = "";
        let currentLabel = "";
        let currentConfidence = 0;

        tokens.forEach((t, index) => {
        // ดึง label ที่ confidence สูงสุดจาก all_probs
        const highestLabel = Object.entries(t.all_probs).reduce(
            (max, [label, prob]) => prob > max.prob ? { label, prob } : max,
            { label: "", prob: 0 }
        );

        // ข้าม label ที่เป็น "O"
        if (highestLabel.label === "O") return;

        if (t.token.startsWith("##")) {
            currentToken += t.token.replace("##", "");
        } else {
            // alert("Token: " + currentToken + " | Label: " + currentLabel + " | Confidence: " + currentConfidence);
            if (currentToken) {
                // push token ก่อนหน้า
                merged.push({
                    token: currentToken,
                    label: currentLabel,
                    confidence: currentConfidence,
                });
            }
            // เริ่ม token ใหม่
            currentToken = t.token;
            currentLabel = highestLabel.label;
            currentConfidence = highestLabel.prob;
        }

        // กรณี token สุดท้าย
        if (index === tokens.length - 1) {
            if (currentToken) {
                merged.push({
                    token: currentToken,
                    label: currentLabel,
                    confidence: currentConfidence,
                });
            }
        }
    });

    return merged;
};

const mergedTokens = mergeTokens(data);

const result = {};
const entLabel = [];
const entConf = [];
const textWithEntities = mergedTokens.map((t, idx) => {
    if(!entLabel.includes(t.label)) {
      entLabel.push(t.label); 
      entConf.push(t.confidence);
    }else if(t.confidence > entConf[entLabel.indexOf(t.label)]) {
      entConf[entLabel.indexOf(t.label)] = t.confidence;
    }
    return result[idx] = {
        label: t.label,
        text: t.token,
        confidence: t.confidence
    };
}); //.join("#ENT#");

const getPriority = (entities) => {
    const equipmentKeywordsHigh = [
        'อินเทอร์เน็ต', 'internet', 'wi-fi', 'wifi', 'ไวไฟ', 'เครื่องสำรองไฟ', 'เครื่อง ups', 'ups',
        'เครื่องคอมพิวเตอร์ตั้งโต๊ะ', 'คอมพิวเตอร์notebook', 'เครื่องปรับอากาศ', 'air', 'แอร์', 'notebook', 'คอมพิวเตอร์โน้ตบุ๊ค',
        'wi fi', 'air containing', 'aircontaining', 'เครื่องโปรเจคเตอร์', 'projector', 'สายhdmi', 'สายvga',
        'เก้าอี้', 'ช่องเสียบสายสัญญาณอินเทอร์เน็ต', 'ช่องเสียบสายแลน', 'เมาส์', 'mouse', 'ไวท์บอร์ด',
        'เครื่องพิมพ์เอกสาร', 'เครื่องprint', 'printer', 'เครื่องพิมพ์', 'เครื่องprinter', 'เมาส์', 'mouse', 'คีย์บอร์ด', 'keyboard',
        'กระดาน', 'whiteboard', 'กระดานไวท์บอร์ด', 'โปรเจคเตอร์', 'จอคอมพิวเตอร์', 'monitor', 'สายแลน', 'คอม',
        'เบรกเกอร์', 'breaker', 'ups', 'สายชาร์จ', 'powerbank', 'power bank', 'คอมพิวเตอร์', 'หน้าจอ',
        'คอมพิวเตอร์โน้ตบุ๊ก', 'โน้ตบุ๊ก', 'laptop', 'หน้าจอคอมพิวเตอร์', 'เครื่องคอมพิวเตอร์', 'ชักโครก',
        'vpn', 'ไมค์โครโฟน', 'ไมโครโฟน', 'ลำโพง', 'speaker', 'แป้นพิมพ์', 'keyboard', 'เมาส์',
        'หลอดไฟ', 'หลอดไฟฟ้า', 'ลิฟต์', 'ปุ่มกดลิฟต์', 'อุปกรณ์', 'device', 'ห้องน้ำ', 'โต๊ะเรียน', 'ซอฟต์แวร์'
    ];
    const issueHigh = [
        'เปิดไม่ติด', 'เปิดไม่ได้', 'ใช้งานไม่ได้', 'ทำงานไม่ได้', 'ไม่ทำงาน', 'เชื่อมต่อไม่ได้', 'ไม่สามารถเชื่อมต่อได้', 'ไม่สามารถใช้งานได้',
        'ไม่สามารถเปิดได้', 'พัง', 'ชำรุด', 'เสีย', 'ไม่พิมพ์', 'ไม่แสดงผล', 'หมึกหมด', 'off', 'trip', 'ทริป', 'แบตเตอรี่หมด', 'แบตเตอรี่ไม่ชาร์จ',
        'แบตเตอรี่ไม่ทำงาน', 'ไฟดูด', 'ใช้อินเทอร์เน็ตไม่ได้', 'หน่วยความจำเต็ม', 'ไม่ติด', 'ไม่ได้', 'พิมพ์ไม่ได้',
    ];
    const issueMedium = [
        'ขาดๆหายๆ', 'ติดๆดับๆ', 'มาๆหายๆ', 'ทำงานช้า', 'สีเพี้ยน', 'สีไม่ปกติ', 'ภาพเบลอ',
        'เสียงดัง', 'มีเสียงดัง', 'มีเสียง', 'กระพริบ', 'ติดตั้งไม่สำเร็จ', 'ติดตั้งซอฟต์แวร์ไม่ได้', 'แบตเตอร์รี่เสื่อม', 'แบตเตอรี่เสื่อม',
        'ติดตั้งโปรแกรมไม่ได้', 'ติดตั้งโปรแกรมไม่สำเร็จ', 'ติดตั้งโปรแกรมไม่เสร็จ', 'ไม่พร้อมใช้งาน', 'สัญญาณไม่ดี', 'สัญญาณไม่ค่อยดี',
    ];
    const issueLow = [
        'ไม่ชัด', 'ไม่ค่อยชัด',
        'ลบไม่สะอาด', 'สัญญาณอ่อน', 'ไม่ชัด', 'ภาพเบลอ', 'สัญญาณค่อนข้างอ่อน', 'ไม่เสถียร', 'พื้นที่จำกัด', 'ไม่สะดวกในการใช้งาน', 'ไม่เย็น',
        'สัญญาณอ่อน', 'เก่า', 'ไม่สะอาด', 'เสียงไม่ดัง', 'เสียงไม่ชัด', 'ใช้งานไม่ดี', 'ใช้ได้บางครั้ง', 'แสดงผลได้ไม่ดี', 'แสดงผลไม่ดี',
        'แสดงผลไม่ชัดเจน', 'แสดงผลไม่ชัด', 'แสดงผลไม่ค่อยชัด', 'แสดงผลไม่ค่อยชัดเจน', 'หมึกจาง', 'เกิดปัญหา', 'มีน้ำหยด', 'น้ำหยด', 'ใช้งานได้ไม่ดี',
        'สัญญาณไม่เสถียร', 'สัญญาณไม่ค่อยเสถียร', 'สัญญาณไม่ค่อยแรง', 'สัญญาณไม่แรง', 'โหลดซอฟต์แวร์ช้า', 'ความเร็วลดลง', 'ใช้งานสะดุด',
    ];

    const equipmentTexts = entities
        .filter(e => e.label === 'B-EQUIPMENT')
        .map(e => e.token.toLowerCase());
    const issueTexts = entities
        .filter(e => e.label === 'B-ISSUE')
        .map(e => e.token.toLowerCase());

    console.log("Equipment: " + JSON.stringify(equipmentTexts) + "\nIssue: " + JSON.stringify(issueTexts));

    // Rule: High
    if (
        equipmentTexts.some(p => equipmentKeywordsHigh.some(pk => p.includes(pk))) &&
        issueTexts.some(i => issueHigh.some(ih => i.includes(ih)))
    ) {
        return "High";
    }

    // Rule: Medium
    if (issueTexts.some(i => issueMedium.some(im => i.includes(im)))) {
        return "Medium";
    }

    // Rule: Low
    if (issueTexts.some(i => issueLow.some(il => i.includes(il)))) {
        return "Low";
    }

    return "Unknown";
}

const priority = getPriority(mergedTokens);

const addItem = async (formInput, priority) => {
  if (!formInput || !priority) {
    alert("กรุณากรอกข้อมูลคำร้องขอบริการและการจัดลำดับความสำคัญ!");
    return;
  }
  try {
    // สถานะเริ่มต้น (เช่น 10 สำหรับ "เปิดคำร้อง", 20 สำหรับ "รับคำร้อง", 30 สำหรับ "ไม่รับคำร้อง", 40 สำหรับ "กำลังดำเนินการ", 50 สำหรับ "ปิดคำร้อง")
    let objSr = {
      SrCreated: serverTimestamp(),
      SrCreatedBy: "zpHahY3AcpoKKFWYyzRG",
      SrDescription: formInput,
      SrId: "SR-" + Math.floor(Math.random() * 1000000),
      SrNote: "",
      SrPriority: priority,
      SrStatus: 10,
      SrUpdated: null,
      SrUpdatedBy: ""
    };
    await addDoc(collection(db, "ServiceRequest"), objSr);
    console.log(objSr);
    console.log("Document successfully written!");
  } catch (err) {
    alert("การบันทึกคำร้องขอบริการเกิดข้อผิดพลาด!");
    console.error("Error adding document: ", err);
  } finally {
    alert("บันทึกคำร้องขอบริการสำเร็จ!");
    setText({
        "SrCreated" : serverTimestamp(),
        "SrCreatedBy" : "",
        "SrDescription" : "",
        "SrId" : "",
        "SrNote" : "",
        "SrPriority" : "",
        "SrStatus" : 10,
        "SrUpdated" : null | "0000-00-00 00:00:00",
        "SrUpdatedBy" : ""
    });
  }
};

let isMounted = true;

useEffect(() => {
  if (isMounted) {
    addItem(inputText, priority);
    isMounted = false;
  }

  return () => {
    isMounted = false;
  };
}, []);

return (
  <div style={{ margin: "auto", width: "100%", padding: "1rem", border: "none", borderRadius: "5px" }}>
    <label>
      <i class="fa fa-search" style={{ color: "#40c6ed" }}></i>
      <span style={{ marginLeft: "5px", fontWeight: "bold" }}> การวิเคราะห์คำร้องขอบริการ (Service Request Analysis)</span>
    </label>
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "1rem", marginBottom: "2rem" }}>
      <thead>
        <tr style={{ backgroundColor: "#f2f2f2" }}>
          <th style={{ borderCollapse: "collapse", borderTop:"2px solid #CCC", borderBottom:"2px solid #CCC", padding: "3px" }}>Token</th>
          <th style={{ borderCollapse: "collapse", borderTop:"2px solid #CCC", borderBottom:"2px solid #CCC", padding: "3px" }}>Label</th>
          <th style={{ borderCollapse: "collapse", borderTop:"2px solid #CCC", borderBottom:"2px solid #CCC", padding: "3px" }}>Confidence</th>
        </tr>
      </thead>
      {
        textWithEntities.map((ent, idx) => {
          if(entLabel.includes(ent.label) && entConf.includes(ent.confidence)) {
            return (
              <tr key={idx}>
                <td style={{ borderCollapse: "collapse", borderBottom:"1px solid #CCC", padding: "5px" }}><span className={`entity ${ent.label}`}>{ent.text}</span></td>
                <td style={{ borderCollapse: "collapse", borderBottom:"1px solid #CCC", padding: "5px", alignContent: "center" }}>{ent.label}</td>
                <td style={{ borderCollapse: "collapse", borderBottom:"1px solid #CCC", padding: "5px", alignContent: "center" }}>{ent.confidence.toFixed(4)}</td>
              </tr>
            );
          }
        })
      }
    </table>
    <i class="fa fa-sort-numeric-asc" style={{ color: "#40c6ed" }}></i>
    <span style={{ marginLeft: "5px", fontWeight: "bold" }}> การจัดลำดับความสำคัญคำร้องขอบริการ (Service Request Priority)</span>
    <div style={{ marginTop: "1rem" }} class={priority}>
      <strong>Priority</strong>: {priority}<br/>
    </div>
  </div>);
};

export default NERText;
