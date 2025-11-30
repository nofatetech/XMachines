<?php

namespace App\Providers;

use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Foundation\Support\Providers\RouteServiceProvider as ServiceProvider;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\Facades\Route;

class RouteServiceProvider extends ServiceProvider
{
    /**
     * The path to your application's "home" route.
     *
     * Typically, users are redirected here after authentication.
     *
     * @var string
     */
    public const HOME = '/';

    /**
     * Define your route model bindings, pattern filters, and other route configuration.
     */
    public function boot(): void
    {
        RateLimiter::for('api', function (Request $request) {
            return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
        });

        $this->routes(function () {
            Route::middleware('api')
                ->prefix('api')
                ->group(function () {
                    $apiRoutesPath = base_path('routes/api.php');
                    \Illuminate\Support\Facades\Log::debug("API Routes path: " . $apiRoutesPath); // Log the path
                    if (file_exists($apiRoutesPath)) {
                        require $apiRoutesPath;
                    } else {
                        \Illuminate\Support\Facades\Log::error("API Routes file not found: " . $apiRoutesPath);
                    }
                });

            Route::middleware('web')
                ->group(base_path('routes/web.php'));
        });
    }
}
