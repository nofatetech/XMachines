@extends('layout')

@section('title')
    Home
@endsection

@section('content')

    <h1>Hello, XMachines!</h1>
    <p>
        Go to the <a href="/dashboard">Dashboard</a>.
        Go to the <a href="/machine_display">Machine Display</a>.
    </p>


    <!-- <h1>Dashboard</h1> -->
    <!-- <p>Welcome, { { auth()->user()->name }}</p> -->

    <!-- <form method="POST" action="/logout">
        @csrf
        <button type="submit">Logout</button>
    </form> -->


@endsection
