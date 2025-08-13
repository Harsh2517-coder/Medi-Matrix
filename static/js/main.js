// static/js/main.js

document.addEventListener('DOMContentLoaded', function() {

    // --- Logic for the Dynamic Appointment Booking Form ---
    const bookingForm = document.getElementById('booking-form');

    // This code will only run if the booking form exists on the current page
    if (bookingForm) {
        // Read the doctor data stored in the form's data-* attribute
        const allDoctors = JSON.parse(bookingForm.dataset.doctors);
        
        const specializationSelect = document.getElementById('specialization');
        const doctorSelect = document.getElementById('doctor');

        specializationSelect.addEventListener('change', function() {
            const specId = this.value;
            
            // Clear existing doctor options
            doctorSelect.innerHTML = '<option selected disabled value="">Choose a doctor...</option>';

            // Filter doctors based on the selected specialization
            const filteredDoctors = allDoctors.filter(doctor => doctor.SpecializationID == specId);
            
            // Populate the doctor dropdown with the filtered list
            filteredDoctors.forEach(doctor => {
                const option = document.createElement('option');
                option.value = doctor.DoctorID;
                option.textContent = `Dr. ${doctor.FirstName} ${doctor.LastName}`;
                doctorSelect.appendChild(option);
            });
        });
    }


    // --- Logic for Decline Appointment Confirmation ---
    const declineButtons = document.querySelectorAll('.btn-decline');

    declineButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Ask the user for confirmation before proceeding
            const isConfirmed = confirm('Are you sure you want to decline this appointment? This action cannot be undone.');
            
            if (!isConfirmed) {
                // If the user clicks "Cancel", prevent the link from being followed
                event.preventDefault();
            }
        });
    });

});