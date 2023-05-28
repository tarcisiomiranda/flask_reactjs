import React, { useState } from 'react';
import { toast } from "react-toastify";
import styled from "styled-components";
import Divisao from "../components/Divisao";
import Navbar from '../components/NavBar';
import axios from 'axios';

const FormContainer = styled.form`
  display: flex;
  align-items: flex-end;
  gap: 40px;
  flex-wrap: wrap;
  background-color: #fff;
  padding: 20px;
  box-shadow: 0px 0px 5px #ccc;
  border-radius: 5px;
`;

const InputArea = styled.div`
  display: flex;
  flex-direction: column;
`;

// const TextArea = styled.textarea`
//   width: 100%;
//   padding: 10px;
//   border: 1px solid #bbb;
//   border-radius: 5px;
//   height: 200px; /* Ajuste a altura conforme necessário */
// `;

const TextArea = styled.textarea`
  width: 400px;
  max-width: 800px;
  height: 400px;
  padding: 10px;
  border: 1px solid #bbb;
  border-radius: 5px
`;

// const Input = styled.input`
//   width: 120px;
//   padding: 0 10px;
//   border: 1px solid #bbb;
//   border-radius: 5px;
//   height: 40px;
// `;

const Label = styled.label``;

const Button = styled.button`
  padding: 10px;
  cursor: pointer;
  border-radius: 5px;
  border: none;
  background-color: #2c73d2;
  color: white;
  height: 42px;
`;

const Table = styled.table`
  width: 100%;
  background-color: #fff;
  padding: 20px;
  box-shadow: 0px 0px 5px #ccc;
  border-radius: 5px;
  min-width: 80%;
  max-width: 1120px;
  margin: 20px auto;
  word-break: break-all;
`;

export const Thead = styled.thead``;

export const Tbody = styled.tbody``;

export const Tr = styled.tr``;

export const Th = styled.th`
  text-align: start;
  border-bottom: inset;
  padding-bottom: 5px;

//   @media (max-width: 500px) {
//     ${(props) => props.onlyWeb && "display: none"}
//   }
`;

const Badge = styled.span`
  padding: 0px 5px;
  border-radius: 5px;
  color: white;
  font-weight: bold;
`;

function Escolha() {
  const [inputData, setInputData] = useState({
    name: '',
    number: 1
  });
  const [tableData, setTableData] = useState([]);

  const handleChange = (event) => {
    setInputData({
      ...inputData,
      [event.target.name]: event.target.value
    });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
        const response = await axios.post('http://localhost:8800/api/escolha', {
          names: inputData.name,
          number: inputData.number
        });
        const data = response.data.message;
        // console.log('|----------> ', data.);
        setTableData(data);

        toast.success('Lista gerada com sucesso.');

      } catch (error) {
        toast.error(error.response.data.message);
      }
      console.log(tableData);
    };

  return (
    <>
      <Navbar />
      {/* <div> */}
        <FormContainer onSubmit={handleSubmit}>
            <Label>
            Names:
            <InputArea>
                <TextArea
                type="text"
                name="name"
                value={inputData.name}
                onChange={handleChange}
                />
            </InputArea>
            </Label>

            <Label>
                Number:
                <InputArea>
                {/* <input
                    type="number"
                    name="number"
                    min={2}
                    max={4}
                    value={inputData.number}
                    onChange={handleChange}
                /> */}
                <Divisao />
                </InputArea>
            </Label>
            <Button type="submit">Sortear</Button>
        </FormContainer>
      {/* </div> */}

      {/* <div> */}
            {tableData.length > 0 && (
                <Table>
                <Thead>
                    <Tr>
                    <Th>Lista</Th>
                    <Th>Nome</Th>
                    <Th>Time</Th>
                    </Tr>
                </Thead>
                <Tbody>
                    {tableData
                    .sort((a, b) => a.time.localeCompare(b.time))
                    .map((item, index) => {
                    const id = Object.keys(item)[0];
                    const name = item[id];
                    const time = item['time'];
                    let badgeColor = '';
                    if (time === 'Time: 1') {
                      badgeColor = '#355C7D';
                    } else if (time === 'Time: 2') {
                        badgeColor = '#6C5B7B';
                    } else if (time === 'Time: 3') {
                        badgeColor = '#F8B195';
                    } else {
                      badgeColor = '#BB405C';
                    }

                    return (
                        <tr key={index}>
                        <td>{id}</td>
                        <td>{name}</td>
                        <Badge style={{ backgroundColor: badgeColor }}>
                            {time}
                        </Badge>
                        </tr>
                    );
                })}
                </Tbody>
                </Table>
            )}
      {/* </div> */}

    </>
  );
}

export default Escolha;
