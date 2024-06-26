// app/components/EventForm.js
import React, { useState } from 'react';

const EventForm = ({ onSubmit }) => {
  const [formData, setFormData] = useState({
    day: '',
    time: '',
    name: '',
    duration: '',
    notes: '',
    all_day: 'no',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Day:
        <input type="text" name="day" value={formData.day} onChange={handleChange} />
      </label>
      <br />
      <label>
        Time:
        <input type="time" name="time" value={formData.time} onChange={handleChange} />
      </label>
      <br />
      <label>
        Event Name:
        <input type="text" name="name" value={formData.name} onChange={handleChange} />
      </label>
      <br />
      <label>
        Duration (hours):
        <input type="number" name="duration" value={formData.duration} onChange={handleChange} />
      </label>
      <br />
      <label>
        Notes:
        <textarea name="notes" value={formData.notes} onChange={handleChange} />
      </label>
      <br />
      <label>
        All-day Event:
        <select name="all_day" value={formData.all_day} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <br />
      <button type="submit">Add Event</button>
    </form>
  );
};

export default EventForm;
