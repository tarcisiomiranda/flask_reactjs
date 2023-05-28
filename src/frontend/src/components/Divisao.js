import React, { useState } from 'react';
import Select from 'react-select'

const Divisao = () => {
  const options = [
    { value: 2, label: '2' },
    { value: 3, label: '3' },
    { value: 4, label: '4' }
  ];

  const [selectedOption, setSelectedOption] = useState(null);

  const handleChange = (selectedOption) => {
    setSelectedOption(selectedOption);
  };

  return (
    <div>
      <Select
        options={options}
        value={selectedOption}
        onChange={handleChange}
        min={2}
        max={4}
      />
    </div>
  );
};

export default Divisao;