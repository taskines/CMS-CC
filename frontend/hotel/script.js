
const API_URL = "https://vm2208.kaj.pouta.csc.fi:8812"

let API_KEY= localStorage.getItem ('hotel_api_key');
if(!API_KEY){
    API_KEY=prompt ("Ge din api_key tack!")
}
async function getBookings() {
    const resp = await fetch(`${API_URL}/bookings`);
    const bookings = await resp.json();

    let bookingsHtml = "";
    for (b of bookings) {
        bookingsHtml += `
            <li>${b.datefrom} Room: ${b.room_number} Guest: ${b.room_type}
            <b> ${b.addinfo || '' }</b>
            <select id="stars-${b.id}">
            <option>   * </option>
            <option>   ** </option>
            <option>  ***  </option>
            <option> ****   </option>
            <option>  *****  </option>
            </select>
            </li>
        `;
    }
    document.querySelector('#bookings').innerHTML = bookingsHtml;
}
getBookings();


async function createBooking() {
    // Detta ska POST:as till /bookings
    const booking = {
        room: document.querySelector('#room').value,
        guest: document.querySelector('#guest').value,
        datefrom: document.querySelector('#datefrom').value
    }
    console.log(booking);
    const resp = await fetch(`${API_URL}/bookings`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(booking)
    })
    const respData = await resp.json();
    getBookings();
    console.log(respData);
}


document.querySelector('#btnBook').addEventListener('click', createBooking);



