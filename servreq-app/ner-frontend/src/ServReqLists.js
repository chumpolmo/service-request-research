import React, { useState, useEffect } from 'react';
// Firebase configuration
import { db } from './config/firebaseConfig';
import { collection, addDoc, query, getDocs, deleteDoc, doc, serverTimestamp, orderBy } from 'firebase/firestore';
import ReactPaginate from 'react-paginate';

function ServReqLists() {
    const [itemOffset, setItemOffset] = useState(0);
    const [items, setItems] = useState([]);
    const [currentPage, setCurrentPage] = useState(0);
    const [totalItems, setTotalItems] = useState(0);
    const itemsPerPage = 10;

    const endOffset = itemOffset + itemsPerPage;
    console.log(`Loading items from ${itemOffset} to ${endOffset}`);
    const currentItems = items.slice(itemOffset, endOffset);
    const pageCount = Math.ceil(items.length / itemsPerPage);

    const handlePageChange = (selectedObject) => {
        const newOffset = (selectedObject.selected * itemsPerPage) % items.length;
        console.log(
        `User requested page number ${selectedObject.selected}, which is offset ${newOffset}`
        );
        setItemOffset(newOffset);
        setCurrentPage(selectedObject.selected);
    };

    const fetchItems = async () => {
      const collectionRef = collection(db, "ServiceRequest"); // Replace 'your_collection_name'
      const q = query(collectionRef, orderBy("SrId", "asc")); // Replace 'your_field_name' and 'asc' or 'desc'
      const snapshot = await getDocs(q);
      const data = snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
      setTotalItems(data.length);
      setItems(data);
    };
    
    const deleteItem = async (id) => {
      if (!id) {
        alert("ไม่พบ ID ของคำร้องขอบริการที่ต้องการลบ!");  
        return;
      }
      if (!window.confirm("กำลังลบคำร้องขอบริการรหัส: " + id +"\nคุณแน่ใจหรือไม่ว่าต้องการลบคำร้องขอบริการนี้?")) {
        return;
      }
      await deleteDoc(doc(db, "ServiceRequest", id));
      fetchItems();
    };

    useEffect(() => {
        let isMounted = true;

        if (isMounted) {
            fetchItems();
        }

        return () => {
            isMounted = false;
        };
    }, []);

    return (
    <>
        <div style={{ margin: "5px", padding: "5px", textAlign: "left", fontSize: "1.2rem", padding: "1rem", borderLeft: "10px solid #40c6ed", borderBottom: "1px solid #40c6ed" }}>
            <i className="fa fa-list-ol" style={{ color: "#40c6ed" }}></i>
            <span style={{ marginLeft: "5px", fontWeight: "bold" }}>รายการข้อมูลคำร้องขอบริการ</span>
        </div>
        <div style={{ padding: "1rem", justifyContent: "center", textAlign: "center" }}>
            <form>
            <input type="text" placeholder="ระบุข้อมูลคำร้องบริการที่ต้องการค้นหา..." 
                style={{ margin: "0.1rem", padding: "0.5rem", fontSize: "1rem", width: "30%", marginRight: "2px", borderRadius: "4px", height: "1rem", border: "1px solid #ccc" }} 
                required={true}
            />
            <button type="submit" style={{ margin: "0.1rem", alignItems: "center", padding: "0.5rem", fontSize: "1rem", backgroundColor: "#40c6ed", border: "none", borderRadius: "4px" }}>
                <i class="fa fa-search"></i> ค้นหา
            </button>
            </form>
        </div>
        <div style={{ padding: "1rem" }}>
            <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: "0.5rem" }}>
                <thead>
                    <tr style={{ backgroundColor: "#f2f2f2" }}>
                    <th style={{ borderCollapse: "collapse", borderTop:"2px solid #CCC", borderBottom:"2px solid #CCC", padding: "5px" }}>รหัสคำร้อง</th>
                    <th style={{ borderCollapse: "collapse", borderTop:"2px solid #CCC", borderBottom:"2px solid #CCC", padding: "5px" }}>รายการคำร้อง</th>
                    <th style={{ borderCollapse: "collapse", borderTop:"2px solid #CCC", borderBottom:"2px solid #CCC", padding: "5px" }}>ความสำคัญ</th>
                    <th style={{ borderCollapse: "collapse", borderTop:"2px solid #CCC", borderBottom:"2px solid #CCC", padding: "5px" }}>สถานะคำร้อง</th>
                    <th style={{ borderCollapse: "collapse", borderTop:"2px solid #CCC", borderBottom:"2px solid #CCC", padding: "5px" }}>ดำเนินการ</th>
                    </tr>
                </thead>
                <tbody>
                {
                    items.length === 0 && (
                        <tr>
                            <td colSpan="5" style={{ textAlign: "center", padding: "1rem", color: "#888" }}>*** ไม่มีข้อมูลคำร้องขอบริการ ***</td>
                        </tr>
                    )
                }
                {
                    currentItems.map((item, idx) => (
                        <tr key={idx}>
                            <td style={{ borderCollapse: "collapse", borderBottom:"1px solid #CCC", padding: "3px", textAlign: "center" }}>{item.SrId}</td>
                            <td style={{ borderCollapse: "collapse", borderBottom:"1px solid #CCC", padding: "3px", textAlign: "left" }}>{item.SrDescription}</td>
                            <td style={{ borderCollapse: "collapse", borderBottom:"1px solid #CCC", padding: "3px", textAlign: "center" }}><span className={`entity ${item.SrPriority}`}>{item.SrPriority}</span></td>
                            <td style={{ borderCollapse: "collapse", borderBottom:"1px solid #CCC", padding: "3px", textAlign: "center" }}>{item.SrStatus}</td>
                            <td style={{ borderCollapse: "collapse", borderBottom:"1px solid #CCC", padding: "3px", textAlign: "center", margin: "auto" }}>    
                                <button onClick={() => deleteItem(item.id)} style={{ margin: "0.1rem", alignItems: "center", padding: "0.5rem", fontSize: "1rem", backgroundColor: "#00e6ac", border: "none", borderRadius: "4px" }}><i class="fa fa-file-text-o"></i> รายละเอียด</button>
                                <button onClick={() => deleteItem(item.id)} style={{ margin: "0.1rem", alignItems: "center", padding: "0.5rem", fontSize: "1rem", backgroundColor: "#ffc34d", border: "none", borderRadius: "4px" }}><i class="fa fa-edit"></i> แก้ไข</button>
                                <button onClick={() => deleteItem(item.id)} style={{ margin: "0.1rem", alignItems: "center", padding: "0.5rem", fontSize: "1rem", backgroundColor: "#ff4d4d", border: "none", borderRadius: "4px" }}><i class="fa fa-trash-o"></i> ลบ</button>
                            </td>
                        </tr>
                    ))
                }
                <tr>
                    <td colSpan="5">
                    <ReactPaginate
                        previousLabel={`<`}
                        nextLabel={`>`}
                        pageCount={Math.ceil(totalItems / itemsPerPage)}
                        onPageChange={handlePageChange}
                        activeClassName={"my-active"}
                        renderOnZeroPageCount={null}
                        containerClassName={'my-pagination'}
                        activeLinkClassName={'my-active'}
                    />
                    </td>
                </tr>
                </tbody>
                </table>
                <span style={{ fontSize: "0.8rem", color: "#888" }}>
                    <i class="fa fa-info-circle" style={{ color: "#40c6ed" }}></i>
                    <span style={{ marginLeft: "5px" }}> หมายเหตุ: 10 - เปิดคำร้อง, 20 - รับคำร้อง, 30 - ไม่รับคำร้อง, 40 - กำลังดำเนินการ และ 50 - ปิดคำร้อง</span>
                </span>
        </div>
    </>
    );
}

export default ServReqLists;