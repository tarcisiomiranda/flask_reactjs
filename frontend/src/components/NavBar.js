import React from 'react';
import { Link } from 'react-router-dom';
import styled from "styled-components";


const Nav = styled.nav`
  width: 100%;
  max-width: 800px;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
`;

const Li = styled.li`color: #fff`;

const Ul = styled.ul`list-style-type: none;
margin: 0;
padding: 0;
color: #fff !important;
`

const Navbar = () => {
  return (
    <Nav style={{ display: 'flex', justifyContent: 'center' }}>
      <Ul style={{ display: 'flex', justifyContent: 'center' }}>
        <Li style={{ padding: '10px' }}>
            <Link style={{color: '#fff'}} to="/">Home</Link>
        </Li>
        <Li style={{ padding: '10px' }}>
            <Link style={{color: '#fff'}} to="/escolha">Escolha</Link>
        </Li>
      </Ul>
    </Nav>
  );
};

export default Navbar;
