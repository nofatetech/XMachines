<!-- machine display view -->
<div class="card bg-base-100 shadow-xl">
    <div class="card-body">
        <h2 class="card-title">Machine: {{ $machine->name }}</h2>
        <p><strong>ID:</strong> {{ $machine->id }}</p>
        <p><strong>Status:</strong> 
            @if ($machine->is_online)
                <span class="badge badge-success">Online</span>
            @else
                <span class="badge badge-error">Offline</span>
            @endif
        </p>
    </div>
</div>
