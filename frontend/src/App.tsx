import { Routes, Route } from 'react-router-dom';
import Committees from './pages/Committees'
import Championships from './pages/Championships'
import ChampionshipDetails from './pages/ChampionshipDetails'
import './index.css';

const App = () => {
  return (
    <div className='app w-full flex flex-col items-center justify-center m-0 p-0 h-fit'>
      <Routes>
        <Route path="/committees" element={<Committees />} />
        <Route path="/committees/:id" element={<Championships />} />
        <Route path="/committees/:committee_id/:id" element={<ChampionshipDetails />} />
      </Routes>
    </div>
  );
};

export default App;
