<x-guest-layout>
    <div class="min-h-screen flex flex-col sm:justify-center items-center pt-6 sm:pt-0 bg-gray-100 dark:bg-gray-900">
        <div class="w-full sm:max-w-md mt-6 px-6 py-4 bg-white dark:bg-gray-800 shadow-md overflow-hidden sm:rounded-lg text-center">
            <h1 class="text-5xl font-bold text-primary mb-4 animate-pulse">KoolRC</h1>
            <p class="text-lg text-gray-700 dark:text-gray-300 mb-6">Your Gateway to Autonomous Machines.</p>

            <div class="space-y-4">
                @auth
                    @if(env('APP_MODE') === 'MACHINE')
                        <a href="{{ route('machine.display') }}" class="btn btn-primary btn-lg w-full">Go to Display</a>
                    @else
                        <a href="{{ route('dashboard') }}" class="btn btn-primary btn-lg w-full">Go to Dashboard</a>
                    @endif
                @else
                    @if (Route::has('login'))
                        <a href="{{ route('login') }}" class="btn btn-primary btn-lg w-full">Login</a>
                    @endif

                    @if (Route::has('register'))
                        <a href="{{ route('register') }}" class="btn btn-secondary btn-lg w-full">Register</a>
                    @endif
                @endauth
            </div>

            <p class="mt-8 text-sm text-gray-500 dark:text-gray-400">Built with Laravel, Reverb & DaisyUI.</p>
        </div>
    </div>
</x-guest-layout>
