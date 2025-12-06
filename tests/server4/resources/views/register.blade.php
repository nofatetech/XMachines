<form method="POST" action="/register">
    @csrf
    <label>Name</label>
    <input type="text" name="name">

    <label>Email</label>
    <input type="email" name="email">

    <label>Password</label>
    <input type="password" name="password">

    <label>Confirm Password</label>
    <input type="password" name="password_confirmation">

    <button type="submit">Register</button>

    @if($errors->any())
      <p>{{ $errors->first() }}</p>
    @endif
</form>
