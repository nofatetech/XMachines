<!-- <div class="uk-card uk-card-default uk-card-body uk-width-1-2@m">
    <h3 class="uk-card-title">Default</h3>
    <p>Lorem ipsum <a href="#">dolor</a> sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
</div> -->

<div class="div_machine_card">
    <div class="card-body">
        <h2 class="card-title">{{ $machine->name }}</h2>
        <p>Status: {{ $machine->status }}</p>
        <div class="card-actions">
            <a href="/machines/{{ $machine->id }}" class="btn btn-primary">View Details</a>
        </div>
    </div>
</div>
