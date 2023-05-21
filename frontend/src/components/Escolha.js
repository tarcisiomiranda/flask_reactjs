import React, { useState } from 'react';
import { toast } from "react-toastify";
import styled from "styled-components";
import axios from 'axios';

const FormContainer = styled.form`
  display: flex;
  align-items: flex-end;
  gap: 20px;
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

const TextArea = styled.textarea`
  width: 120px;
  padding: 10px;
  border: 1px solid #bbb;
  border-radius: 5px;
  height: 200px; /* Ajuste a altura conforme necessário */
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

function Escolha() {
  const [inputData, setInputData] = useState({
    name: ''
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
          names: inputData.name
        });
        const data = response.data.message;
        console.log('|----------> ', data);
        setTableData(data);
        toast.success(data.message);
      } catch (error) {
        toast.error(error.response.data);
      }
      console.log(tableData);
    };

  return (
    <>
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
        <Button type="submit">Submit</Button>
      </FormContainer>

      {tableData.length > 0 && (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
            </tr>
          </thead>
          <tbody>
            {tableData.map((item, index) => {
              const id = Object.keys(item)[0];
              const name = item[id];

              return (
                <tr key={index}>
                  <td>{id}</td>
                  <td>{name}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      )}

    </>
  );
}

export default Escolha;
