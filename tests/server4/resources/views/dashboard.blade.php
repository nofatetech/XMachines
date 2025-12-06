@extends('layout')

@section('title')
    Dashboard
@endsection

@section('content')

    <h1>Dashboard!</h1>
    <p>
        Go <a href="/">Home</a>.
    </p>

    <div class="xxuk-flex">
        @foreach ($machines as $machine)
            @include('machine_card', ['machine' => $machine])
        @endforeach
    </div>

@endsection
