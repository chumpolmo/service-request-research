import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './Home';
import SerReqListsPage from './ServReqLists';

function App() {
  return (
    <Router>
      <div style={{ margin: "0px", textAlign: "center", fontSize: "1rem", padding: "1rem", backgroundColor: "#40c6ed" }}>
        <i className="fa fa-commenting"></i> 
        <span style={{ marginLeft: "5px", fontWeight: "bold" }}>Automated Prioritization for Monitoring and Tracking Service Requests</span>
      </div>
      <nav>
        <ul>
          <li>
            <Link to="/"><i className='fa fa-home'></i> หน้าแรก</Link>
          </li>
          <li>
            <Link to="/home"><i className="fa fa-comment-o"></i> กรอกข้อมูลคำร้อง</Link>
          </li>
          <li>
            <Link to="/servreqlists"><i className="fa fa-list-ol"></i> รายการข้อมูลคำร้อง</Link>
          </li>
          <li>
            <Link to="/"><i className="fa fa-info-circle"></i> เกี่ยวกับงานวิจัย</Link>
          </li>
          <li>
            <Link to="/"><i className="fa fa-envelope-o"></i> ติดต่อเรา</Link>
          </li>
          <li style={{ float: "right" }}>
            <div className="dropdown">
              <Link className="dropbtn"><i className="fa fa-user-circle-o"></i> Administrator</Link>
              <div className="dropdown-content">
                <Link to="/"><i className="fa fa-address-card-o"></i> โปรไฟล์</Link>
                <Link to="/"><i className="fa fa-key"></i> เปลี่ยนรหัสผ่าน</Link>
                <Link to="/"><i className="fa fa-power-off"></i> ออกจากระบบ</Link>
              </div>
            </div>
          </li>
        </ul>
      </nav>

      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/servreqlists" element={<SerReqListsPage />} />
      </Routes>
      <div style={{ textAlign: "center", fontSize: "0.8rem", marginTop: "2rem", marginBottom: "2rem", borderTop: "1px solid #ccc", paddingTop: "1rem" }}>
        <span>© 2025 Chumpol Mokarat, Pattarak Sawatdee, and Pimpika Intusing</span>
        <br />
        <span>Version: 1.0</span>
        <br />
        <span>Contact: <a href="mailto:chumpol_mo@rmutto.ac.th" className='aLink'>chumpol_mo@rmutto.ac.th</a></span>
      </div>
    </Router>
  );
}

export default App;