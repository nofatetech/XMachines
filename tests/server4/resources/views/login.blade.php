<form method="POST" action="/login">
    @csrf
    <label>Email</label>
    <input type="email" name="email">

    <label>Password</label>
    <input type="password" name="password">

    <button type="submit">Login</button>

    @if($errors->any())
      <p>{{ $errors->first() }}</p>
    @endif
</form>
