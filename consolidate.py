{% extends "layout.html" %} {% block title %}Pallet planner{% endblock %} {%
block body %}

<div class="container">
  <div class="row">
    <div class="col">
      <h1>Pallet planner</h1>
      <hr />
      <form action="/upload-load" method="POST" enctype="multipart/form-data">
        <div class="form_group">
          <label style="font-size: 1em"
            >What is the load number you would like to plan? (must have 6
            digits)</label
          ><br />
          <br />
          <input type="text" size="6" id="load_number" name="load_number" />
          <br />
          <br />
          <label style="font-size: 1em"
            >Add csv file with load which needs planing pallets: <br />(file
            needs to be called <span class="inside">"load.csv"</span>, must have
            2 columns without headers: 1st column SKU, 2nd column
            quantity)</label
          >
          <br />
          <br />
          <div class="custom-file">
            <input
              type="file"
              class="custom-file-input"
              name="load"
              id="load"
            />
            <br />
            <br />
            <label>Do you want to consolidate orders?</label>
            <input
              type="checkbox"
              name="consolidate"
              id="consolidate"
              checked
            /><br />
            <br />
            <label class="custom-file-label"></label>
          </div>
        </div>
        <br />
        <button type="submit" class="btn btn-primary">Upload load</button>
      </form>
    </div>
  </div>
</div>
{% endblock %}
